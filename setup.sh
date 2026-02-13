#!/bin/bash

echo "🚀 Setting up Educational Platform..."

# Create backend virtual environment
echo "📦 Setting up Python backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create environment file
echo "⚙️  Creating .env file..."
cp .env.example .env

echo ""
echo "✅ Backend setup complete!"
echo ""
echo "📋 Next steps:"
echo ""
echo "1. Install PostgreSQL (if not already installed):"
echo "   brew install postgresql  # macOS"
echo "   # or download from https://www.postgresql.org/download/"
echo ""
echo "2. Create the database:"
echo "   createdb edu_platform"
echo ""
echo "3. Update backend/.env with your database credentials"
echo ""
echo "4. Start the backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python app.py"
echo ""
echo "5. In another terminal, start the frontend:"
echo "   cd frontend"
echo "   npm install"
echo "   npm run dev"
echo ""
echo "6. Open http://localhost:3000 in your browser"
echo ""
echo "🎉 Happy coding!"
