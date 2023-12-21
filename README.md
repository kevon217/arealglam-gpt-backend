# README.md

# Project Overview

This project involves developing a Python backend application integrated with OpenAI's GPT assistants, primarily for a fashion recommendation platform. The system, built using FastAPI, is designed to interact with a React/Next.js frontend. The core functionality revolves around handling user queries about fashion, with the backend orchestrating responses from multiple GPT assistants.

# Project Design/Architecture

- **Backend Framework:** FastAPI, supporting asynchronous operations with AsyncIO.
- **GPT Assistants:** Utilizes three custom OpenAI GPT assistants (Orchestrator, Psychologist, and Wardrobe).
- **OpenAI Functional Calls:** Utilizes a parallel function chat completion endpoint to extract product details from the Orchestrator's suggestion, which are then passed to the Wardrobe Assistant for product search and product ID retrieval.
- **WebSocket Communication:** Implemented for real-time interaction between backend and frontend.
- **Docker Deployment:** Containerized backend for deployment, ensuring environment consistency.
- **AWS Deployment:** Backend application deployed on a Docker container hosted on AWS EC2 instance, ensuring cloud-based WebSocket communication.

# What We've Done

1. **Developed Core Backend Logic:** Services and endpoints created in FastAPI to interact with GPT assistants.
2. **AsyncThread Implementation:** Built an AsyncThread class for communication with OpenAI assistants, managing threads, messages, and runs.
3. **WebSocket Setup:** Established WebSocket logic for real-time data transmission to the frontend.
4. **Integration Testing:** Conducted tests for proper message passing and response retrieval from OpenAI assistants.
5. **Environment Setup:** Configured environment variables and OpenAI client for API interactions.
6. **Dockerization:** Containerized the backend application for deployment.
7. **Frontend Integration Coordination:** Coordinated with the frontend developer for seamless integration, focusing on request handling and WebSocket communication.
8. **Testing in Docker Environment:** Tested the complete system within a Docker container to ensure stability and performance.
9. **AWS Deployment and Testing:** Deployed and tested the system in a Docker container on AWS EC2 for cloud websocket communication.

# What Remains

10. **Performance Optimization:** Analyzing response times and optimizing backend efficiency.
11. **Error Handling and Edge Case Testing:** Implementing robust error handling and testing for edge cases.
12. **Production Deployment Readiness:** Finalizing the application for production, including security enhancements and scalability considerations.
13. **Frontend State Management:** Ensuring proper state management on the frontend to sync with backend operations.

# Notes for the Frontend Developer

- **WebSocket Integration:** The backend uses WebSocket for real-time communication. Ensure the frontend can establish and maintain a stable WebSocket connection.
- **Handling Backend Responses:** Backend sends JSON formatted responses. Parse these responses appropriately in the frontend for display and interaction.
- **Environment Consistency:** Maintain consistency in environment variables and configurations between frontend and backend.
