# Day Trading Academy

A full-stack educational platform for learning day trading fundamentals with a premium course and Stripe integration.

## Tech Stack

- **Frontend**: React + TypeScript, React Router, TailwindCSS
- **Backend**: Node.js + Express
- **Database**: PostgreSQL
- **Authentication**: Email/password with JWT
- **Payments**: Stripe Checkout (test mode)

## Setup Instructions

### Prerequisites

- Node.js (v18+)
- PostgreSQL
- Stripe account (for test keys)

### Environment Setup

Create `.env` files in both `client/` and `server/` using the provided `.env.example` files.

### Running the App

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
client/
├── public/
├── src/
│   ├── components/
│   ├── pages/
│   ├── App.tsx
│   └── index.tsx
└── .env

server/
├── src/
│   ├── controllers/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── middleware/
│   └── index.ts
├── prisma/
│   └── schema.prisma
└── .env
```
