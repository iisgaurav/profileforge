# Component Architecture

ProfileForge uses a component-based rendering tree that abstracts away the underlying SVG markup.

## Base Components

- **Card**: The foundational container for all widgets.
- **Text**: For rendering typography with token-based sizing and colors.
- **Icon**: For rendering vector icons.
- **Badge**: Small labels and status indicators.
- **ProgressBar**: Visualizing metrics and completion.
- **Chart**: Base charts like line, bar, and pie charts.

## Layout Components

- **Flex**: For flexbox-like linear layouts (row/column).
- **Grid**: For coordinate-based placement.

All components automatically map to the active theme's design tokens.
