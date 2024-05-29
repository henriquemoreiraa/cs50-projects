# Violin Sheet Music 🎻

This project is designed to provide a platform for violin players to share their performance recordings with a community of users, who can then rate and provide feedback on these attempts. The main objective is to create a supportive environment for violinists to improve their skills and share their musical journeys.

## Distinctiveness and Complexity

This project stands out due to its unique features, including file uploads, filtering options, and a rating mechanism.

### File Uploads

- **Image Upload**: Users can upload image files, such as sheet music or photos related to their performance, directly from their computers. This feature allows for the sharing of visual aids that can enhance the understanding of the performance.
- **Audio Upload**: Users can upload audio recordings of their violin performances. A custom validator ensures that the uploaded files are indeed audio files, preventing any incorrect file types from being uploaded. This feature is critical for sharing and evaluating musical performances.

### Filters

- **Index Page**: A search mechanism allows users to find specific content.
- **Sheet Page**: Users can filter attempts by date or ratings using a dropdown menu.

### Ratings:

- **User Ratings**: After a user uploads a performance attempt, other users can listen to the recording and provide ratings.

## Custom Files

This project includes several files that were not part of any course projects:

- **templatetags**: Custom Django template tags.
- **forms**: ModelForms for handling form data.
- **validators**: Custom validators to ensure file integrity and type.

## How to Run the Application

To get started with the application, follow these steps:

```bash
# Install dependencies
$ pip install -r requirements.txt

# Make migrations
$ python manage.py makemigrations

# Apply migrations
$ python manage.py migrate

# Run the server
$ python manage.py runserver
```
