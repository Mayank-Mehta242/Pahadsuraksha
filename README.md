# PahadSuraksha

## AI-Based Landslide Risk Prediction and Disaster Awareness System

**PahadSuraksha** is an AI-based landslide risk prediction and disaster awareness platform designed to improve road safety and disaster preparedness in hilly regions of Uttarakhand.

The platform uses **weather conditions, terrain information, and historical landslide data** to assess the potential risk of landslides for a given location or route. It presents the risk in a simple and understandable way so that citizens, particularly **drivers and people travelling through hilly roads**, can make safer travel decisions.

Along with risk prediction, PahadSuraksha allows citizens to **report landslide incidents**, which can be reviewed and verified by authorized authorities. Verified incidents can then contribute to public awareness and future risk monitoring.

The initial focus of the platform is **Tehri Garhwal, Uttarakhand**.

---

# Problem Statement

Landslides are a major challenge in hilly regions of Uttarakhand, especially during heavy rainfall and monsoon seasons. People travelling through mountain roads often do not have easy access to understandable and location-specific information about potential landslide risks.

Existing information may be scattered across multiple sources, difficult to interpret, or unavailable when users need it most.

There is a need for a platform that can:

* Analyze environmental and weather-related conditions.
* Estimate potential landslide risk.
* Present risk information in a simple format.
* Help travellers make safer decisions.
* Allow citizens to report incidents.
* Enable authorities to review and verify reported incidents.
* Improve public awareness about road and disaster conditions.

PahadSuraksha aims to address these challenges through an integrated platform for **risk prediction, incident reporting, authority verification, and public awareness**.

---

# Main Objective

The primary goal of PahadSuraksha is to provide **timely, understandable, and location-specific landslide risk information** to improve road safety and disaster awareness in Uttarakhand.

The platform aims to help users understand potential risks before and during travel and encourage better communication between citizens and authorized authorities.

---

# Core Flow

## Landslide Risk Prediction

**Weather Data + Terrain Information + Historical Landslide Data**

↓

**Data Processing and Risk Analysis**

↓

**AI/ML Risk Prediction**

↓

**Landslide Risk Level**

↓

**Safety Recommendation and Public Awareness**

## Incident Reporting

**Citizen Reports Incident**

↓

**Incident Submitted to System**

↓

**Authority Reviews Report**

↓

**Approve or Reject**

↓

**Verified Incident Shared for Public Awareness**

---

# Key Features

## 1. Landslide Risk Prediction

The platform analyzes relevant environmental and weather conditions to estimate the potential landslide risk for a location or route.

Possible risk categories include:

* Safe Journey
* Low Risk
* Moderate Risk
* Risky
* High Landslide Risk

The risk level is presented in a simple format to help users understand the situation.

---

## 2. Weather Information

Users can view relevant weather information that may affect travel and landslide risk.

The system can analyze factors such as:

* Rainfall
* Temperature
* Humidity
* Wind Speed
* Weather Conditions

Weather information can contribute to the overall risk analysis.

---

## 3. Route and Location-Based Risk Awareness

Users can provide information such as:

* Source Location
* Destination Location
* Selected Route

The platform can use available information to provide location-specific risk awareness and safety recommendations.

---

## 4. Interactive Map

The platform uses map-based visualization to help users understand locations and road conditions.

Possible map features include:

* Location visualization
* Route information
* Incident locations
* Risk zones
* Important road safety information

---

## 5. Citizen Incident Reporting

Citizens can report landslide-related incidents through the platform.

A report may include:

* Incident Title
* Location
* Severity Level
* Description
* Photo or Video Evidence

Severity categories may include:

* Low
* Medium
* High
* Very High

---

## 6. Authority Review System

Authorized authorities can review submitted incident reports.

Authorities can:

* View submitted incidents
* Review incident details
* Verify available information
* Approve incidents
* Reject invalid reports

This helps improve the reliability of public information.

---

## 7. Public Awareness

Once an incident is verified, relevant information can be used to increase public awareness.

Possible awareness mechanisms include:

* Dashboard alerts
* Public notifications
* Route warnings
* Awareness messages
* Future messaging channel integration

---

## 8. User Authentication and Roles

The platform supports different user roles.

### Citizen

Citizens can:

* Register and log in
* Check landslide risk
* View weather information
* Report incidents
* Access safety recommendations

### Disaster Authority

Authorized authorities can:

* Log in securely
* Review reported incidents
* Approve or reject reports
* Monitor verified incidents
* Support public awareness

---

# System Architecture

```text
                         USERS
                           |
            --------------------------------
            |                              |
         Citizen                    Disaster Authority
            |                              |
            --------------------------------
                           |
                    React Frontend
                           |
                    REST API Requests
                           |
                    Flask Backend
                           |
        ----------------------------------------
        |                  |                   |
        |                  |                   |
   Authentication      Risk Analysis      Incident System
        |                  |                   |
        |                  |                   |
      JWT/Auth         AI/ML Model       Report Management
        |                  |                   |
        ----------------------------------------
                           |
                    Data Processing
                           |
        -----------------------------------------
        |                  |                    |
        |                  |                    |
    Weather API       Landslide Data       Terrain Data
        |                  |                    |
        -----------------------------------------
                           |
                       Database
                           |
                Users | Incidents | Results
```

---

# Architecture Explanation

## Frontend Layer

The frontend provides the interface through which users interact with PahadSuraksha.

Technologies:

* React
* Vite
* CSS
* React Router

Main interfaces include:

* Home Page
* Dashboard
* Weather Page
* Incident Reporting Page
* Login and Registration
* Authority/Admin Panel

---

## Backend Layer

The backend handles application logic and communication between the frontend, database, external APIs, and AI/ML components.

Possible technologies:

* Flask
* Python
* REST APIs

The backend manages:

* User authentication
* Weather data
* Risk prediction requests
* Incident reports
* Authority review
* Database operations
* API integration

---

## AI/ML Layer

The AI/ML component analyzes relevant information to estimate potential landslide risk.

Possible input factors include:

* Rainfall
* Temperature
* Humidity
* Wind Speed
* Terrain Information
* Historical Landslide Data

The processed information is passed to a machine learning model.

Possible model:

* Random Forest Classifier

The model produces a risk category based on the available data.

---

## Data Layer

The system stores and manages application data.

Possible stored data includes:

* User Information
* User Roles
* Incident Reports
* Incident Status
* Risk Predictions
* Historical Data

Possible database:

* PostgreSQL
* SQLite for development

---

## External Services

PahadSuraksha may use external services for:

### Weather Data

Weather APIs can provide:

* Rainfall information
* Temperature
* Humidity
* Wind Speed
* Weather Conditions

### Maps

Map services can provide:

* Location visualization
* Route information
* Geographic data

Possible technologies:

* Leaflet
* OpenStreetMap

---

# Application Workflow

## Complete User Workflow

```text
User Opens PahadSuraksha
            |
            v
     Selects Required Feature
            |
    --------------------------
    |                        |
Risk Prediction        Report Incident
    |                        |
    v                        v
Enter Location/Route    Fill Incident Details
    |                        |
    v                        v
Fetch Weather Data      Submit Report
    |                        |
    v                        v
Process Input Data      Store in Database
    |                        |
    v                        v
AI/ML Risk Analysis     Authority Review
    |                        |
    v                  ----------
Generate Risk Level     |        |
    |                Approve   Reject
    v                  |
Show Safety             v
Recommendation     Public Awareness
```

---

# Landslide Risk Prediction Workflow

```text
User Selects Location or Route
              |
              v
      Weather Data Collected
              |
              v
     Additional Data Processed
              |
              v
      Data Sent to AI/ML Model
              |
              v
      Landslide Risk Predicted
              |
              v
      Risk Category Generated
              |
              v
     Safety Recommendation Shown
```

---

# Incident Reporting Workflow

```text
Citizen
   |
   v
Submit Incident Report
   |
   v
Report Stored in Database
   |
   v
Status: Pending Review
   |
   v
Authority Reviews Report
   |
   +-------------------+
   |                   |
   v                   v
Approve              Reject
   |                   |
   v                   v
Verified Incident    Report Closed
   |
   v
Public Awareness
   |
   v
Dashboard / Alerts / Notifications
```

---

# Technology Stack

## Frontend

* React
* Vite
* JavaScript
* CSS
* React Router
* Axios

## Backend

* Python
* Flask
* REST APIs

## Artificial Intelligence and Machine Learning

* Python
* Scikit-learn
* Random Forest
* Data Processing

## Database

* SQLite for development
* PostgreSQL for production

## Maps

* Leaflet
* OpenStreetMap

## External APIs

* Weather API
* Location and Map Services

## Authentication

* JWT
* Secure Password Handling

## Version Control

* Git
* GitHub

---

# Project Structure

```text
PahadSuraksha/
│
├── frontend/
│   │
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── styles/
│   │   └── App.jsx
│   │
│   └── package.json
│
├── backend/
│   │
│   ├── app.py
│   ├── config.py
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   ├── weather.py
│   │   ├── incidents.py
│   │   └── prediction.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── incident.py
│   │   └── prediction.py
│   │
│   ├── services/
│   │   ├── weather_service.py
│   │   └── prediction_service.py
│   │
│   └── ml/
│       ├── dataset/
│       └── model/
│
├── README.md
└── requirements.txt
```

---

# User Roles

## Citizen

A citizen can:

* Register and log in
* Check weather conditions
* View landslide risk information
* Enter route details
* Report incidents
* View safety recommendations
* Access public awareness information

---

## Disaster Authority

An authorized authority can:

* Log in securely
* View submitted incidents
* Review incident reports
* Approve incidents
* Reject invalid reports
* Monitor verified incidents

---

# Risk Levels

The system can present landslide risk using understandable categories.

| Risk Level          | Description                                                          |
| ------------------- | -------------------------------------------------------------------- |
| Safe Journey        | Conditions currently indicate relatively lower risk                  |
| Low Risk            | Some environmental factors should be monitored                       |
| Moderate Risk       | Users should travel carefully and monitor conditions                 |
| Risky               | Travel requires increased caution                                    |
| High Landslide Risk | High-risk conditions detected; users should avoid unnecessary travel |

Risk predictions should be treated as **decision-support information and not as a replacement for official disaster warnings or emergency instructions**.

---

# Future Improvements

Future development may include:

* Real-time landslide alerts
* WhatsApp awareness channel integration
* SMS notifications
* Improved route-based risk prediction
* Government data integration
* Satellite and remote sensing data
* Advanced terrain analysis
* More accurate machine learning models
* Real-time monitoring dashboard
* Mobile application
* Emergency contact integration
* Historical risk visualization
* Community verification mechanisms
* Advanced authority dashboard

---

# Development Roadmap

## Phase 1: Basic Platform

* User interface
* Authentication
* Weather integration
* Basic risk display
* Incident reporting

## Phase 2: Authority System

* Authority dashboard
* Incident review
* Approval and rejection workflow
* Verified incident management

## Phase 3: AI/ML Integration

* Data collection
* Data preprocessing
* Machine learning model
* Risk prediction
* Model evaluation

## Phase 4: Public Awareness

* Public alerts
* Verified incident visibility
* Safety recommendations
* Awareness notifications

## Phase 5: Advanced System

* Real-time monitoring
* Improved prediction models
* Government integration
* Advanced geographic analysis
* Mobile application

---

# Project Vision

The long-term vision of PahadSuraksha is to develop a technology-driven disaster awareness and road safety platform that helps people make more informed decisions while travelling through landslide-prone regions.

The platform aims to combine:

* Artificial Intelligence
* Weather Data
* Geographic Information
* Historical Landslide Data
* Citizen Participation
* Authority Verification

to create a more connected and informed approach to disaster awareness.

---

# Disclaimer

PahadSuraksha is designed as a decision-support and disaster awareness platform.

The risk predictions and recommendations generated by the system should not replace official warnings, instructions, or emergency advisories issued by government authorities and disaster management organizations.

Users should always follow official emergency guidance and local authority instructions.

---

# Contributing

Contributions are welcome.

To contribute:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Test the changes.
5. Create a pull request.

Please ensure that contributions are relevant to the project and properly documented.

---

# Project Summary

**PahadSuraksha is an AI-based landslide risk prediction and disaster awareness platform that uses weather conditions, terrain information, and historical landslide data to provide understandable risk information for travellers. The platform also enables citizens to report incidents and allows authorized authorities to verify reports before contributing to public awareness and future disaster monitoring.**
