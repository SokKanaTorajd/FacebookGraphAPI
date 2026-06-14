# Facebook & Instagram Graph API Integrator

A Python backend module built to communicate with the Facebook Graph API, specifically designed to navigate the complex authentication flow required to extract data from linked Instagram Business accounts.

## The Challenge
Accessing Instagram data via the official Graph API requires a strict, multi-layered authentication sequence. This module automates that process to seamlessly retrieve data without manual intervention.

## Key Features
*   **Multi-Step Authentication Flow:** Automatically handles the sequence of retrieving the FB User ID -> Linked FB Page ID -> Linked Instagram Account ID -> Final API Token.
*   **Data Retrieval:** Fetches insights and social data directly from the authenticated Instagram endpoint.
*   **Endpoint Maintenance:** Structured to allow easy updates for deprecating API versions (a common occurrence within the Facebook developer ecosystem).

## Context
This repository serves as the official API integration layer for a broader social media data pipeline. It was built with strict adherence to Facebook's developer testing scenarios and app review processes.

## Tech Stack
*   Python
*   Facebook Graph API
*   RESTful Architecture
