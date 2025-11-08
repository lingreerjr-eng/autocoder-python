# Day Trading Learning Platform

A full-stack web application to learn day trading with a structured course, free resources, and payment integration.

## Features

- Modern React frontend with TypeScript
- Node.js + Express backend with REST API
- Stripe integration for course purchase
- User authentication and progress tracking
- Responsive UI with TailwindCSS

## Setup

### Prerequisites

- Node.js (v16+)
- MongoDB instance (local or cloud)

### Environment Variables

Create `.env` files in both `client/` and `server/` directories based on `.env.example` files.

### Running the Application

#### Backend

```bash
cd server
npm install
npm run dev
```

#### Frontend

```bash
cd client
npm install
npm start
```

## Project Structure

```
├── client/
│   ├── public/
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── services/
│       └── App.tsx
├── server/
│   ├── src/
│   │   ├── controllers/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── app.ts
│   ├── .env.example
│   └── package.json
└── README.md
```
