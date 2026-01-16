# CraftLet Server Documentation

## Overview

CraftLet Server is a FastAPI-based backend service designed for managing and sharing project templates sourced from GitHub repositories. The server provides authentication via GitHub OAuth, template CRUD operations, and supports mobile app integration through deep linking.

### Key Features

- **GitHub OAuth Authentication**: Secure user authentication using GitHub accounts
- **Template Management**: Create, read, update, and delete project templates from GitHub repositories
- **Advanced Filtering**: Search templates by name, author, and tags
- **Pagination**: Cursor-based pagination for efficient data retrieval
- **Mobile Integration**: Android app links and deep linking support
- **JWT Security**: Token-based authentication for protected endpoints
- **MongoDB Storage**: NoSQL database for scalable data management

### Technology Stack

- **Framework**: FastAPI (Python 3.12+)
- **Database**: MongoDB (via Motor async driver)
- **Authentication**: GitHub OAuth 2.0, JWT
- **Caching**: Redis
- **Deployment**: Docker, Uvicorn ASGI server
- **Package Management**: uv (Astral)

## Architecture

### Project Structure

```
src/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── digitalAsset.py      # Android app links endpoint
│   ├── api/
│   │   └── v1/
│   │       ├── dependency.py    # Database dependency injection
│   │       ├── route/           # API route handlers
│   │       │   ├── auth.py      # Authentication endpoints
│   │       │   └── template.py  # Template management endpoints
│   │       ├── schema/          # Pydantic data models
│   │       │   ├── auth/        # Authentication schemas
│   │       │   ├── githubApi/   # GitHub API schemas
│   │       │   ├── template/    # Template schemas
│   │       │   └── user/        # User schemas
│   │       └── service/         # Business logic services
│   │           ├── authService.py
│   │           ├── githubService.py
│   │           └── templateService.py
│   ├── core/
│   │   ├── client.py        # GitHub OAuth client
│   │   ├── decorator.py     # Endpoint type decorators
│   │   ├── enum.py          # Endpoint type enumerations
│   │   ├── middleware.py    # Authentication middleware
│   │   └── utils/
│   │       └── jwt.py       # JWT utilities
│   └── db/
│       ├── __init__.py      # Database connection management
│       └── model/           # Database models
│           ├── customTypes.py
│           ├── template.py
│           └── user.py
```

### Application Flow

1. **Authentication**: Users authenticate via GitHub OAuth
2. **Token Generation**: JWT tokens are issued upon successful authentication
3. **Template Operations**: Authenticated users can manage templates
4. **Data Persistence**: All data is stored in MongoDB
5. **Mobile Integration**: Deep links redirect users to mobile app

## Installation and Setup

### Prerequisites

- Python 3.12 or higher
- MongoDB instance
- Redis instance
- GitHub OAuth App credentials
- GitHub Personal Access Token (fine-grained)

### Environment Configuration

Create a `.env` file in the project root with the following variables:

```env
# GitHub OAuth Settings
auth.github_auth_settings.client_id=your_github_client_id
auth.github_auth_settings.client_secret=your_github_client_secret
auth.github_auth_settings.authorize_url=https://github.com/login/oauth/authorize
auth.github_auth_settings.token_url=https://github.com/login/oauth/access_token
auth.github_auth_settings.api_base=https://api.github.com

# GitHub API Settings
api.github_api_settings.fine_grained_pat=your_github_pat

# MongoDB Settings
db.mongo_db_settings.db_name=craftlet_db
db.mongo_db_settings.db_password=your_mongodb_password
db.mongo_db_settings.db_username=your_mongodb_username
db.mongo_db_settings.db_host=cluster0.xxxxx.mongodb.net
db.mongo_db_settings.app_name=craftlet

# Application Settings
app_settings.session_secret_key=your_session_secret
app_settings.jwt_secret_key=your_jwt_secret
app_settings.jwt_algorithm=HS256

# Digital Asset Settings
digital_asset_settings.deeplink_settings.android_fingerprint=your_sha256_fingerprint
```

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd craftlet-server
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Configure environment**:
   - Copy `.env.example` to `.env`
   - Fill in all required environment variables

4. **Run the application**:
   ```bash
   uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

### Docker Deployment

Build and run using Docker:

```bash
docker build -t craftlet-server .
docker run -p 8000:8000 --env-file .env craftlet-server
```

## API Documentation

### Authentication Endpoints

#### GitHub OAuth Login
- **Endpoint**: `GET /api/v1/auth/github/login`
- **Description**: Initiates GitHub OAuth flow
- **Response**: Redirect to GitHub authorization page

#### GitHub OAuth Callback
- **Endpoint**: `GET /api/v1/auth/github/callback`
- **Description**: Handles OAuth callback, creates/updates user, issues JWT
- **Response**: Redirect to mobile app with JWT token

### Template Management Endpoints

All template endpoints require authentication (Bearer token in Authorization header).

#### Get Template List
- **Endpoint**: `POST /api/v1/template/`
- **Description**: Retrieve paginated list of templates with optional filtering
- **Request Body**:
  ```json
  {
    "templateNamePrefix": "string",
    "templateAuthorNamePrefix": "string",
    "templateTags": ["tag1", "tag2"]
  }
  ```
- **Query Parameters**: `cursor` (optional, for pagination)
- **Response**: `TemplatePage` with data, nextCursor, hasMore

#### Create Template
- **Endpoint**: `POST /api/v1/template/createTemplate`
- **Description**: Create a new template from a GitHub repository
- **Request Body**:
  ```json
  {
    "templateLink": "https://github.com/owner/repo",
    "description": "Optional description",
    "tags": ["tag1", "tag2"]
  }
  ```
- **Response**: Success message

#### Update Template
- **Endpoint**: `PATCH /api/v1/template/updateTemplate`
- **Description**: Update template tags or description
- **Request Body**:
  ```json
  {
    "templateId": "template_id",
    "addTags": ["new_tag"],
    "removeTags": ["old_tag"],
    "description": "Updated description"
  }
  ```
- **Response**: Update confirmation

#### Delete Template
- **Endpoint**: `DELETE /api/v1/template/deleteTemplate?templateId={id}`
- **Description**: Delete a template by ID
- **Response**: Deletion confirmation

#### Get Template Detail
- **Endpoint**: `GET /api/v1/template/templateDetail?templateId={id}`
- **Description**: Get detailed information about a specific template
- **Response**: `TemplateOut` object

### Digital Asset Endpoints

#### Android App Links
- **Endpoint**: `GET /.well-known/assetlinks.json`
- **Description**: Provides Android app link configuration for deep linking
- **Response**: JSON configuration for Android app associations

## Data Models

### User Models

#### UserInDb
```python
class UserInDb(BaseModel):
    id: PyObjectId
    email: str
    githubId: int
    githubUsername: str
    githubAvatarUrl: str | None
    githubProfilePage: str | None
```

#### UserOut
```python
class UserOut(BaseModel):
    username: str
    githubProfile: str | None
    githubAvatarUrl: str | None
```

### Template Models

#### TemplateIn
```python
class TemplateIn(BaseModel):
    templateLink: str
    description: str | None
    tags: List[str]
```

#### TemplateOut
```python
class TemplateOut(BaseModel):
    name: str
    tags: List[str]
    useCount: int
    version: str
    description: str
```

#### TemplateInDb
```python
class TemplateInDb(BaseModel):
    id: PyObjectId
    authorId: str
    name: str
    authorName: str
    originalLink: str
    description: str | None
    version: str
    useCount: int
    tags: List[str]
    createdAt: datetime
```

#### TemplateFilter
```python
class TemplateFilter(BaseModel):
    templateNamePrefix: str | None
    templateAuthorNamePrefix: str | None
    templateTags: List[str] | None
```

#### TemplatePage
```python
class TemplatePage(BaseModel):
    data: List[TemplateListElement]
    nextCursor: str | None
    hasMore: bool
```

#### TemplateUpdate
```python
class TemplateUpdate(BaseModel):
    templateId: str
    addTags: List[str] | None
    removeTags: List[str] | None
    description: str | None
```

### GitHub Integration Models

#### GithubUser
```python
class GithubUser(BaseModel):
    id: int
    login: str
    avatarUrl: str | None
    htmlUrl: str | None
```

#### GithubEmail
```python
class GithubEmail(BaseModel):
    email: str
    primary: bool
    verified: bool
```

#### RepositoryDetail
```python
class RepositoryDetail(BaseModel):
    id: str
    name: str
    repoLink: str
    description: str | None
    isFork: bool
    forkCount: int
    createdAt: datetime
```

## Database Schema

### Collections

#### users
- Stores user information linked to GitHub accounts
- Indexed on `githubId` (unique)

#### templates
- Stores template information
- No specific indexes defined beyond default `_id`

### Custom Types

#### PyObjectId
- Wrapper for MongoDB ObjectId with Pydantic validation
- Automatically converts string IDs to ObjectId instances

## Security

### Authentication
- GitHub OAuth 2.0 for user authentication
- JWT tokens for API access
- Session-based OAuth state protection

### Authorization
- Endpoint-level protection using decorators (`@protected`, `@public`, `@private`)
- Middleware validates JWT tokens on protected routes
- User context injected into request state

### Data Protection
- Environment variables for sensitive configuration
- CORS configuration for cross-origin requests
- HTTPS enforcement in production

## Services

### AuthService
- Currently empty, reserved for future authentication logic

### GithubService
- `getGithubRepoDetails()`: Fetches repository information from GitHub API
- Uses fine-grained personal access token for authentication
- Returns structured repository data

### TemplateService
- `handleTemplateList()`: Implements filtering and pagination logic
- `createNewTemplate()`: Creates templates from GitHub repositories
- `updateExistingTemplate()`: Updates template metadata
- `deleteExistingTemplate()`: Removes templates
- `getExistingTemplateDetail()`: Retrieves individual template details

## Configuration

### Settings Structure
The application uses Pydantic settings with nested configuration:

- **AuthSettings**: GitHub OAuth configuration
- **ApiSettings**: GitHub API access tokens
- **DbSettings**: MongoDB connection details
- **AppSettings**: JWT and session secrets
- **DigitalAssetSettings**: Android app link fingerprints

### Environment Loading
- Settings loaded from `.env` file in project root
- Nested delimiter: `.`
- UTF-8 encoding
- Automatic validation and type conversion

## Deployment

### Docker Configuration
- Base image: `python:3.12-slim`
- Uses `uv` for fast Python package management
- Exposes port 8000
- Production-ready with optimized layers

### Production Considerations
- Environment variables for configuration
- Connection pooling for MongoDB
- Async operations for scalability
- Proper error handling and logging

## Development

### Running Locally
```bash
# Install dependencies
uv sync

# Run development server
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Testing
- No specific test files identified in current codebase
- Recommended: Add unit tests for services and integration tests for API endpoints

### Code Quality
- Type hints throughout the codebase
- Pydantic models for data validation
- Async/await patterns for concurrency
- Clean separation of concerns (routes, services, models)

## API Versioning

- Current API version: v1
- Version prefix: `/api/v1/`
- Backward compatibility maintained within major versions

## Error Handling

- HTTP exceptions for API errors
- Structured error responses
- Database connection error handling
- OAuth state validation

## Future Enhancements

- User profile management
- Template rating and reviews
- Advanced search capabilities
- Template categories
- Social features (sharing, following)
- API rate limiting
- Comprehensive logging and monitoring
- Unit and integration test suites

---