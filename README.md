# Metstat
A fully autonomous, unattended, solar-powered, IoT weather probe with mesh networking capabilities.

<br><img height="350" alt="image" src="https://github.com/user-attachments/assets/f0d9faf0-f985-42cd-832b-3d01d26774f1" />
<img height="350" alt="image" src="https://github.com/user-attachments/assets/4f75dd7c-1d28-487e-886c-dd3f7bac162d" />


## Hardware stack
| Component  | Part | Notes |
| - | - | - |
| MCU | `STM32L4A6AG` | Low power MCU with small package size, decent connectivity and hardware acceleration for crypto algorithms |
| Power Supply  | `SPV1050` | Integrated energy harvester with Max Power Point Tracking. Managing intake from solar panels and LiPo storage |
| `TODO` | `TODO` | `TODO` |

## Firmware stack
Written in C++, runs on the standard STM32 [HAL](https://www.st.com/resource/en/user_manual/um1725-description-of-stm32f4-hal-and-lowlayer-drivers-stmicroelectronics.pdf) 
using [CubeMX](https://www.st.com/en/development-tools/stm32cubemx.html) (standard runtime for STM32s).

## Technical description
`todo`
