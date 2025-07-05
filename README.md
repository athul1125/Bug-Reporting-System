# Bug Reporting System

A robust Django-based bug tracking system designed to streamline the software development lifecycle through efficient bug management, role-based access control, and comprehensive analytics.

## Core Features

### User Management
- Role-based access control (Developers, Testers, Admins)
- Secure user authentication and authorization
- Profile management with contact information
- Admin controls for user management (create, edit, delete users)

### Bug Management
1. **Bug Reporting**
   - Unique bug identification (auto-generated bug codes)
   - Detailed bug information capture
   - Screenshot attachments
   - Platform classification (Windows, Web, iOS)
   - Contact information tracking

2. **Status Tracking**
   - Multiple status states (Open, In Progress, Fixed, Closed)
   - Precise timestamp tracking:
     - Creation time
     - In-progress time
     - Fix time
     - Closure time
   - Accurate work duration calculations

3. **Assignment System**
   - Developer assignment tracking
   - Last updater tracking
   - Clear ownership and responsibility chain

### Sprint Management
- Sprint creation and management
- Bug-to-sprint association
- Comprehensive sprint analytics:
  - Platform-wise bug resolution times
  - Developer performance metrics
  - Total sprint duration tracking

### Analytics and Reporting
1. **Performance Metrics**
   - Average bug resolution time per platform
   - Developer-wise performance statistics
   - Sprint completion analytics

2. **Data Export/Import**
   - Excel file export functionality
   - Bulk bug data import capability
   - Data validation and error handling

### Role-Specific Views
1. **Tester Features**
   - Bug reporting interface
   - "My Bugs" view for reported bugs
   - Bug closure capability
   - Status tracking

2. **Developer Features**
   - "My Assigned Bugs" view
   - Bug status management
   - Work duration tracking
   - Sprint view access

3. **Admin Features**
   - User management
   - System-wide access
   - Configuration controls

### Technical Features
- Clean, modern, and responsive UI
- Secure data handling
- File upload management
- RESTful API endpoints
- Custom permissions and decorators
- Efficient database queries and annotations

## Security
- Login required for all operations
- Permission-based access control
- CSRF protection
- Secure file handling
- Role-based view restrictions

## Data Management
- Accurate timestamp tracking
- Automatic bug code generation
- File storage for screenshots
- Data validation and sanitization
- Efficient query optimization
