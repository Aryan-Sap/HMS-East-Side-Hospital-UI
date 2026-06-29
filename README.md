# East Side Hospital UI - Hospital Management System

This is a comprehensive Hospital Management System (HMS) developed as a first-year project for East Side Hospital. It provides a robust, graphical User Interface (UI) for managing day-to-day hospital operations, built using Python's `tkinter` library and backed by a SQLite database (`HospitalDB.db`).

## Features

- **Secure Login Authentication:** Uses an external authentication API (via `bsnlpbx.com`) to ensure only authorized personnel can access the system.
- **Main Dashboard:** A centralized menu system connecting all hospital operations.
- **Patient Registration & Management:** Add new patients, record details (blood group, contact, assigned doctor), and view or edit existing patient records.
- **Employee Management:** Register hospital staff, assign designations, track salaries and experience, with full CRUD (Create, Read, Update, Delete) capabilities.
- **Room Allocation:** Assign rooms to patients, select room types (Single, Twin Sharing, Triple Sharing), and automatically track admission and discharge dates.
- **Appointment Booking:** Schedule, view, edit, and delete patient appointments with specific doctors using an integrated calendar UI.
- **Billing System:** Automatically generate comprehensive bills for patients, pulling in room charges, treatment costs, and medicine prices for outstanding balance calculation.

## Technology Stack

- **Frontend Interface:** Python 3 + `tkinter` (with `ttk` for styled widgets).
- **Date Picking:** `tkcalendar` for intuitive calendar dropdowns.
- **Backend Database:** SQLite3 (`HospitalDB.db`)
- **API Integration:** `requests` module for external authentication.

## Getting Started

### Prerequisites

Ensure you have Python 3.x installed. You will also need to install the following dependencies:

```bash
pip install tkcalendar requests pillow
```

### Running the Application

1. Clone this repository.
2. Navigate to the project directory.
3. Run the main login script:
```bash
python login3.py
```
4. Authenticate using your valid credentials to access the main dashboard.

## Database Schema Highlights

The system operates on a relational database featuring the following core tables:
- `PATIENT` and `CONTACT_NO`: Stores patient demographics and contact details.
- `employee`: Tracks all hospital staff details.
- `ROOM`: Manages hospital bed/room occupancy.
- `appointment`: Schedules patient visits with doctors.
- `TREATMENT` & `MEDICINE`: Manages financial costs for billing.

## Project Status

This repository is currently being actively refined and optimized. Upcoming updates will include UI/UX standardization across all modules, improved database connection handling, and advanced code deduplication for better performance.
