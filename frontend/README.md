# FusionForms Frontend

Modern, intuitive Vue.js 3 frontend for the FusionForms platform - an intelligent dynamic form builder with data insights.

## 🚀 Features

### Core Features
- **Drag-and-Drop Form Builder** - Intuitive interface for creating forms
- **Rich Field Library** - 19+ field types including text, email, select, file upload, rating, signature, and more
- **Real-time Form Preview** - See your form as users will see it
- **Advanced Field Properties** - Validation rules, conditional visibility, custom styling
- **Multi-page Forms** - Break complex forms into logical sections
- **Form Analytics Dashboard** - Real-time insights with interactive charts
- **Submission Management** - View, edit, filter, and export submissions
- **Webhook Integration** - Send data to external services
- **Embed Options** - iFrame and JavaScript embed codes
- **Theme Customization** - Industry-grade light/dark theme system with full customization

### User Experience
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- **Modern UI** - Built with Vuetify 3 Material Design components
- **Form State Management** - Save progress and return later
- **Inline Validation** - Real-time feedback on form inputs
- **Success/Error Handling** - Clear feedback for all user actions

## 🛠️ Tech Stack

- **Vue.js 3** - Progressive JavaScript framework with Composition API
- **TypeScript** - Type-safe development
- **Vuetify 3** - Material Design component framework
- **Pinia** - State management
- **Vue Router** - Client-side routing
- **Chart.js** - Data visualization
- **Axios** - HTTP client
- **Vuedraggable** - Drag and drop functionality

## 📋 Prerequisites

- Node.js 20.19.0+ or 22.12.0+
- npm or yarn
- FusionForms backend running (see backend README)

## 🏗️ Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd formfussion/frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and set your backend API URL:
   ```env
   VITE_API_URL=http://localhost:8000/api
   ```

4. **Start development server**:
   ```bash
   npm run dev
   ```

The application will be available at `http://localhost:5173`

## 📦 Available Scripts

```bash
# Development
npm run dev              # Start development server
npm run build            # Build for production
npm run preview          # Preview production build

# Code Quality
npm run lint             # Lint and fix code
npm run format           # Format code with Prettier
npm run type-check       # TypeScript type checking

# Testing
npm run test:unit        # Run unit tests
npm run test:e2e         # Run end-to-end tests
```

## 🏗️ Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── assets/          # Images, styles, etc.
│   ├── components/      # Reusable components
│   │   ├── auth/        # Authentication components
│   │   ├── form-builder/# Form builder components
│   │   │   └── fields/  # Field type components
│   │   └── shared/      # Shared UI components
│   ├── plugins/         # Vue plugins (Vuetify)
│   ├── router/          # Vue Router configuration
│   ├── services/        # API services
│   ├── stores/          # Pinia stores
│   ├── types/           # TypeScript type definitions
│   ├── views/           # Page components
│   │   ├── auth/        # Login, Register
│   │   └── forms/       # Form-related views
│   ├── App.vue          # Root component
│   └── main.ts          # Application entry point
├── .env.example         # Environment variables template
├── package.json         # Dependencies and scripts
├── tsconfig.json        # TypeScript configuration
├── vite.config.ts       # Vite configuration
└── README.md            # This file
```

## 🎨 Key Components

### Form Builder
- **FieldPalette** - Draggable field types library
- **FormCanvas** - Drop zone for form construction
- **FieldProperties** - Configure field settings
- **FormPreview** - Real-time form preview

### Field Components
All field components support:
- `v-model` binding
- Validation rules
- Conditional visibility
- Custom styling
- Help text and placeholders

Supported field types:
- Text, Textarea, Number, Email, URL
- Date, Time
- Checkbox, Radio, Select (single/multi)
- File Upload
- Rating Scale
- Signature
- Rich Text Editor
- Hidden Fields
- Layout elements (Heading, Paragraph, Divider, Image)

### Views
- **Dashboard** - Overview of forms and statistics
- **FormList** - Browse and manage forms
- **FormBuilder** - Create and edit forms
- **FormDetail** - Form overview with tabs
- **FormAnalytics** - Charts and insights
- **FormSubmissions** - View and manage submissions
- **FormSettings** - Configure form behavior
- **FormPreview** - Public form view for submissions

## 🔐 Authentication

The application uses token-based authentication:
1. Users log in with username/password
2. Backend returns authentication token
3. Token stored in localStorage
4. Token sent with all API requests
5. Auto-redirect to login on token expiration

## 📊 State Management

Pinia stores manage application state:

- **authStore** - User authentication and profile
- **formsStore** - Forms data and operations
- **submissionStore** - Submission management
- **snackbarStore** - Global notifications

## 🎯 API Integration

All API calls go through the Axios instance configured in `src/services/api.ts`:

```typescript
import apiClient from '@/services/api'

// Make authenticated requests
const response = await apiClient.get('/forms/')
```

The API client automatically:
- Adds authentication token to requests
- Handles 401 errors (token expiration)
- Provides consistent error handling

## 🌐 Routing

Protected routes require authentication:
```typescript
{
  path: '/forms',
  component: FormList,
  meta: { requiresAuth: true }
}
```

Guest-only routes (login, register):
```typescript
{
  path: '/login',
  component: LoginView,
  meta: { guest: true }
}
```

## 🎨 Theming

Customize the application theme in `src/plugins/vuetify.ts`:

```typescript
const lightTheme: ThemeDefinition = {
  colors: {
    primary: '#1976D2',
    secondary: '#424242',
    accent: '#82B1FF',
    // ... more colors
  }
}
```

## 🚀 Production Build

1. **Build the application**:
   ```bash
   npm run build
   ```

2. **Preview the build**:
   ```bash
   npm run preview
   ```

3. **Deploy**: 
   - Copy `dist/` folder to your web server
   - Configure server for SPA (all routes point to index.html)
   - Set environment variables for production

### Nginx Configuration Example

```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🐛 Troubleshooting

### Build Errors
- Clear node_modules: `rm -rf node_modules && npm install`
- Clear cache: `rm -rf .vite`
- Check Node.js version: `node --version`

### API Connection Issues
- Verify backend is running
- Check VITE_API_URL in `.env`
- Inspect network tab for CORS errors
- Verify backend CORS configuration

### Type Errors
- Run type checking: `npm run type-check`
- Update TypeScript: `npm install -D typescript@latest`

## 📝 Development Guidelines

### Code Style
- Use TypeScript for all new files
- Follow Vue 3 Composition API patterns
- Use Pinia for state management
- Implement proper error handling
- Add JSDoc comments for complex functions

### Component Guidelines
- Keep components focused and reusable
- Use props for data down, events for data up
- Implement proper TypeScript interfaces
- Add validation for user inputs
- Handle loading and error states

### Git Workflow
1. Create feature branch from `main`
2. Make changes with descriptive commits
3. Test thoroughly
4. Submit pull request
5. Address code review feedback

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request

---

**FusionForms** - Intelligent Dynamic Form Builder & Data Insights Platform
