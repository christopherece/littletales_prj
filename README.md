# LittleTales

A child-friendly educational platform built with Django that provides interactive learning experiences and storytelling for young children.

## Features

- Child-friendly user interface with bright colors and playful design
- Educational activities and games for children
- Interactive storytelling platform
- Achievement system with badges and rewards
- Safe and secure environment for children
- Parental controls and monitoring
- Progress tracking for learning activities
- Early learning content tailored for children
- Responsive design optimized for both desktop and mobile

## Installation

1. Clone the repository:
```
git clone <repository-url>
cd LittleTales
```

2. Create and activate a virtual environment:
```
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Set up the database:
```
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser (admin):
```
python manage.py createsuperuser
```

6. Run the development server:
```
python manage.py runserver
```

7. Access the application at `http://127.0.0.1:8000/`

## Usage

1. Create a parent account to manage children's profiles
2. Add child profiles with appropriate age settings
3. Explore educational activities in the "Learning Adventures" section
4. Read and interact with stories in the "Magic of Stories" section
5. Track progress and achievements in the "Achievements" section
6. Monitor child's activity through the parent dashboard
7. Customize learning paths based on child's interests and progress

## Technologies Used

- Django 5.2.1
- Bootstrap 5.3
- Font Awesome 6.0.0
- SQLite (database)
- Custom CSS for child-friendly design
- Responsive design principles
- Python 3.11+

## Project Structure

```
LittleTales/
├── early_learning/      # Main application for educational content
├── socialmedia/         # Social features and user interactions
├── posts/              # Content management
├── users/              # User authentication and profiles
├── chat/               # Communication features
├── templates/          # HTML templates
├── static/             # CSS, JS, and media files
└── littletales/        # Project configuration
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please contact support@littletales.com or create an issue in the GitHub repository.
