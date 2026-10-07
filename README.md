# ESPHome Custom Components

This repository contains custom components for [ESPHome](https://esphome.io/), a system to control ESP32 devices with simple YAML configuration files.

> **Fork note:** This is a fork of [Averyy/esphome-custom-components](https://github.com/Averyy/esphome-custom-components) with VL53L4CD-specific updates to the `vl53l1x` component. See [VL53L4CD Updates](#vl53l4cd-updates-in-this-fork). The other components are unchanged from upstream.

## Available Components

-   [HLK-LD2413](#hlk-ld2413) - 24GHz mmWave radar liquid level sensor
-   [HLK-LD8001H](#hlk-ld8001h) - 80GHz mmWave radar liquid level sensor
-   [Notecard](#notecard) - Blues Wireless Notecard IoT modules
-   [VL53L1X](#vl53l1x) - Time-of-Flight distance sensor

## HLK LD2413

A budget precision liquid level detection sensor using 24GHz millimeter wave radar technology with a detection range of 0.15m to 10.5m and accuracy of ±3mm under optimal conditions. The component enforces all datasheet constraints, including detection range (150mm-10500mm) and report cycle timing (50ms-1000ms).

The LD2413 is very picky about surroundings and reflections. Enclosures or electronics too close to it can cause it to not provide any readings (or provide wildy inaccurate ones). Always test it solo first to help narrow down any issues.

### Installation

```yaml
external_components:
    - source: github://Averyy/esphome-custom-components
      components: [hlk_ld2413]
```

**Resources:**

-   [Documentation](components/hlk_ld2413/README.md)
-   [Example Configuration](example_hlk_ld2413.yaml)
-   Purchase ($20CAD): [AliExpress](https://www.aliexpress.com/item/1005006766564668.html) / [AliExpress 2](https://www.aliexpress.com/item/1005008479449270.html)

## HLK-LD8001H

A high-end precision liquid level detection sensor using 80GHz millimeter wave radar technology with a detection range of 0.15m to 40m and accuracy of ±5mm under optimal conditions. This UART component supports both distance-only mode and water depth calculation when installation height is specified.

The 80GHz technology offers excellent detection capabilities even in challenging environments, making it ideal for water tanks, silos, and other liquid level monitoring applications. It is not picky about enclosures and works fine with a 3D printed case or electronics nearby.

There's an optional lens that narrows the beamwidth to ±3 degrees, whereas without the lens and just the bare sensor it is quite wide at ±25 degrees.

### Installation

```yaml
external_components:
    - source: github://Averyy/esphome-custom-components
      components: [hlk_ld8001h]
```

**Resources:**

-   [Documentation](components/hlk_ld8001h/README.md)
-   [Example Configuration](example_hlk_ld8001h.yaml)
-   Purchase ($50CAD): [AliExpress](https://www.aliexpress.com/item/1005006703020398.html) / [Alibaba](https://www.alibaba.com/product-detail/HLK-LD8001H-80G-liquid-level-detection_1601053500911.html)

## Blues Notecard

Integration with Blues Wireless Notecard (both cellular and WiFi variants) for IoT connectivity. Features include configurable data collection and sync intervals, automatic data batching, and access to Notecard temperature and battery voltage.

The implementation focuses specifically on using the Notecard for data transmission to Notehub, while the ESP32 handles sleep cycles and data filtering for optimal power efficiency.

### Installation

```yaml
external_components:
    - source: github://Averyy/esphome-custom-components
      components: [notecard]
```

**Resources:**

-   [Documentation](components/notecard/README.md)
-   [Example Configuration](example_notecard.yaml)
-   Purchase ($70CAD): [Blues Shop](https://shop.blues.com/collections/notecard)

## TOF400C VL53L1X

Integration with the VL53L1X/VL53L4CD Time-of-Flight (ToF) distance sensor. Supports both VL53L1X and VL53L4CD sensors with configurable distance modes and range status reporting.

This I2C component was forked from an existing open source repository after updates caused compatibility issues with my setup. I created this stable version primarily for water level monitoring applications, though I discovered that lens condensation in humid environments could affect reading stability - an important consideration for similar implementations.

### Installation

```yaml
external_components:
    - source: github://Averyy/esphome-custom-components
      components: [vl53l1x]
```

**Resources:**

-   [Documentation](components/vl53l1x/README.md)
-   [Example Configuration](example_vl53l1x.yaml)

### VL53L4CD Updates in This Fork

The `vl53l1x` component in this fork has been updated to drive the VL53L4CD (sensor ID 0xEBAA) as ST's VL53L4CD driver (STSW-IMG026) does, rather than as a VL53L1X:

-   Loads ST's VL53L4CD default configuration (e.g. 40mm sigma threshold instead of the VL53L1X's 90mm) and performs the extra VL53L4CD init write.
-   Calculates the timing budget from the sensor's oscillator frequency using ST's VL53L4CD formula instead of the VL53L1X tables. The VL53L4CD supports a maximum budget of 200ms, so larger values (including the 500ms default) are clamped to 200ms.

These general fixes apply to both sensors:

-   New `timing_budget` option.
-   Distance mode is set before the timing budget, so short mode gets the short mode timing values.
-   Only new measurements are published, never the same reading twice.
-   Corrected intermeasurement period and VHV register writes.
-   Compiles with current ESPHome versions.

To use this fork's version:

```yaml
external_components:
    - source: github://chadj/esphome-custom-components
      components: [vl53l1x]
```

## General Information

### Features

-   **Easy Integration**: Simple YAML configuration for complex sensors
-   **Fully Documented**: Comprehensive documentation for each component
-   **Example Configurations**: Ready-to-use example files for quick setup

### Note on Installation

Using the GitHub repository version means you'll automatically get updates, but it could change at any moment. If stability is critical for your project, consider using the local installation method described in each component's documentation.

## License

This project is licensed under the MIT License with Attribution - see the [LICENSE](LICENSE) file for details.
