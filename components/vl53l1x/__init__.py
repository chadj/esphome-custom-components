import esphome.codegen as cg # type: ignore 
import esphome.config_validation as cv # type: ignore 
from esphome.components import i2c # type: ignore 
from esphome.const import CONF_ID # type: ignore 

CODEOWNERS = ["@mrtoy-me"]

CONF_VL53L1X_ID = "vl53l1x_id"
CONF_DISTANCE_MODE = "distance_mode"
CONF_TIMING_BUDGET = "timing_budget"

vl53l1x_ns = cg.esphome_ns.namespace("vl53l1x")
DistanceMode = vl53l1x_ns.enum("DistanceMode")

DISTANCE_MODES = {
    "short": DistanceMode.SHORT,
    "long": DistanceMode.LONG, 
}

# Timing budgets (ms) supported by the ST VL53L1X ULD register tables.
# A VL53L4CD (always short mode) computes its timing from ST's VL53L4CD ULD
# formula instead and is limited to 200 ms; larger values are clamped at runtime.
TIMING_BUDGETS = {
    "short": [15, 20, 33, 50, 100, 200, 500],
    "long": [20, 33, 50, 100, 200, 500],
}


def validate_timing_budget(config):
    mode = config[CONF_DISTANCE_MODE]
    budget = config[CONF_TIMING_BUDGET].total_milliseconds
    if budget not in TIMING_BUDGETS[mode]:
        allowed = ", ".join(f"{b}ms" for b in TIMING_BUDGETS[mode])
        raise cv.Invalid(
            f"Timing budget {budget}ms is not supported in {mode} distance mode, "
            f"must be one of: {allowed}",
            path=[CONF_TIMING_BUDGET],
        )
    return config

VL53L1XComponent = vl53l1x_ns.class_(
    "VL53L1XComponent", cg.PollingComponent, i2c.I2CDevice
)

CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(VL53L1XComponent),
            cv.Optional(CONF_DISTANCE_MODE, default="long"): cv.enum(
                DISTANCE_MODES, upper=False
            ),
            cv.Optional(
                CONF_TIMING_BUDGET, default="500ms"
            ): cv.positive_time_period_milliseconds,
        }
    ).extend(cv.polling_component_schema("60s")),
    validate_timing_budget,
)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    cg.add(var.config_distance_mode(config[CONF_DISTANCE_MODE]))
    cg.add(var.config_timing_budget(config[CONF_TIMING_BUDGET].total_milliseconds))
