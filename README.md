# Deperfection - Task Management System

**Developed by EllaimA - Copyright (c) 2025 EllaimA. All rights reserved.**

## Overview

Deperfection is a comprehensive task management application built with Streamlit that helps users follow a structured workflow: Analyze → Prediction → Work → Result → Review.

## Features

- **Analyze Phase**: Define tasks, set goals, and establish baselines
- **Prediction Phase**: Assess worst-case scenarios, create Plan B, and estimate probabilities
- **Work Phase**: Execute tasks with real-time countdown timer and note-taking
- **Result Phase**: Record completion status and quality assessment
- **Review Phase**: Reflect on progress and areas for improvement

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install streamlit streamlit-autorefresh
   ```
3. Run the application:
   ```bash
   streamlit run main.py
   ```

## Database

The application uses SQLite to store task data persistently. Run the migration script if upgrading from an older version:

```bash
python migrate_database.py
```

## License and Copyright

**IMPORTANT COPYRIGHT NOTICE:**

This software is developed by **EllaimA** and is subject to specific licensing terms:

### Source Code
- Licensed under EllaimA Proprietary License with Attribution Requirements
- You must prominently display "Developed by EllaimA - Copyright (c) 2025 EllaimA" in all uses
- Commercial use permitted with proper attribution

### Images and Assets
- **ALL IMAGES, ICONS, AND VISUAL ASSETS ARE PROPRIETARY AND CLOSED SOURCE**
- Owned exclusively by EllaimA
- NOT licensed for redistribution or modification
- Must be replaced if creating derivative works

### Attribution Requirements
Any use of this software must include:
- Copyright notice in all interfaces and documentation
- "Powered by EllaimA Technology" in user interfaces
- Clear attribution to EllaimA as the original developer

## Disclaimer

THIS SOFTWARE IS PROVIDED BY ELLAI A "AS IS" WITHOUT ANY EXPRESS OR IMPLIED WARRANTIES. ELLAI A SHALL NOT BE LIABLE FOR ANY DAMAGES ARISING FROM THE USE OF THIS SOFTWARE.

## Contact

For licensing inquiries or permissions beyond this license, contact EllaimA.

---

**© 2025 EllaimA. All rights reserved.**
