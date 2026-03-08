# Next.js & TypeScript Documentation Conventions

This reference covers best practices for documenting Next.js applications and TypeScript code.

## TypeScript Type Documentation

### JSDoc Comments for Types

```typescript
/**
 * User account information with authentication details.
 * @typedef {Object} User
 * @property {string} id - Unique user identifier
 * @property {string} email - User email address
 * @property {string} name - Full user name
 * @property {Date} createdAt - Account creation timestamp
 * @property {boolean} isActive - Whether account is active
 */
interface User {
  id: string;
  email: string;
  name: string;
  createdAt: Date;
  isActive: boolean;
}
```

### Generic Types

```typescript
/**
 * Response wrapper for API endpoints.
 * @template T The data type contained in the response
 */
interface ApiResponse<T> {
  /** HTTP status code */
  status: number;
  /** Response data */
  data: T;
  /** Error message if applicable */
  error?: string;
}
```

### Enum Documentation

```typescript
/**
 * User role levels in the application.
 * Controls access permissions for different features.
 */
enum UserRole {
  /** Administrator with full access */
  ADMIN = "admin",
  /** Moderator with limited admin functions */
  MODERATOR = "moderator",
  /** Standard user with basic permissions */
  USER = "user",
  /** Guest user with view-only access */
  GUEST = "guest",
}
```

---

## Next.js Components

### Server Components

```typescript
/**
 * Displays a list of blog posts fetched from the database.
 *
 * This is a Server Component that fetches data at build time
 * or on each request. It should not use client-side hooks.
 *
 * @component
 * @example
 * return <BlogPostList revalidate={3600} />
 *
 * @param {Object} props - Component props
 * @param {number} props.limit - Maximum number of posts to display (default: 10)
 * @param {string} props.category - Filter posts by category (optional)
 * @returns {Promise<JSX.Element>} Rendered blog post list
 */
export async function BlogPostList({
  limit = 10,
  category,
}: {
  limit?: number;
  category?: string;
}): Promise<JSX.Element> {
  const posts = await getPosts({ limit, category });

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

### Client Components

```typescript
"use client";

/**
 * Modal dialog component for user interactions.
 *
 * This is a Client Component with interactive features
 * like state management and event handlers.
 *
 * @component
 * @example
 * const [isOpen, setIsOpen] = useState(false);
 * return (
 *   <>
 *     <button onClick={() => setIsOpen(true)}>Open Modal</button>
 *     <Modal isOpen={isOpen} onClose={() => setIsOpen(false)} />
 *   </>
 * )
 */
interface ModalProps {
  /** Whether the modal is visible */
  isOpen: boolean;
  /** Callback when modal should close */
  onClose: () => void;
  /** Modal content title */
  title?: string;
  /** Modal body content */
  children: React.ReactNode;
}

export function Modal({ isOpen, onClose, title, children }: ModalProps) {
  if (!isOpen) return null;

  return (
    <div className="modal">
      <h2>{title}</h2>
      {children}
      <button onClick={onClose}>Close</button>
    </div>
  );
}
```

---

## Next.js API Routes

### Route Handlers (App Router)

```typescript
/**
 * Handles GET requests to fetch paginated user data.
 *
 * Query Parameters:
 * - `page` (number): Page number (default: 1)
 * - `limit` (number): Items per page (default: 20, max: 100)
 *
 * @param {Request} request - The incoming HTTP request
 * @returns {Promise<Response>} JSON response with users and pagination info
 *
 * @example
 * GET /api/users?page=2&limit=50
 * Response: { users: [...], total: 150, page: 2, limit: 50 }
 *
 * @throws {400} If page or limit parameters are invalid
 * @throws {500} If database query fails
 */
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const page = parseInt(searchParams.get("page") || "1");
  const limit = parseInt(searchParams.get("limit") || "20");

  if (page < 1 || limit < 1 || limit > 100) {
    return Response.json({ error: "Invalid parameters" }, { status: 400 });
  }

  try {
    const users = await db.user.findMany({
      skip: (page - 1) * limit,
      take: limit,
    });

    const total = await db.user.count();

    return Response.json({
      users,
      total,
      page,
      limit,
    });
  } catch (error) {
    return Response.json({ error: "Failed to fetch users" }, { status: 500 });
  }
}
```

---

## Server Actions

```typescript
"use server";

/**
 * Creates a new blog post in the database.
 *
 * Server Action that can be called directly from Client Components
 * using the form action property. Automatically handles serialization
 * and runs securely on the server.
 *
 * @param {FormData} formData - Form submission data
 * @param {string} formData.get('title') - Post title
 * @param {string} formData.get('content') - Post content
 * @param {string} formData.get('category') - Post category
 *
 * @returns {Promise<{success: boolean, postId?: string, error?: string}>}
 * Result object indicating success and the new post ID or error message
 *
 * @example
 * <form action={createBlogPost}>
 *   <input name="title" required />
 *   <textarea name="content" required />
 *   <button type="submit">Create Post</button>
 * </form>
 *
 * @throws {Error} If database insert fails
 */
export async function createBlogPost(
  formData: FormData
): Promise<{ success: boolean; postId?: string; error?: string }> {
  try {
    const title = formData.get("title") as string;
    const content = formData.get("content") as string;
    const category = formData.get("category") as string;

    const post = await db.blogPost.create({
      data: { title, content, category },
    });

    return { success: true, postId: post.id };
  } catch (error) {
    return { success: false, error: "Failed to create post" };
  }
}
```

---

## Custom Hooks

```typescript
/**
 * Hook for fetching user data with caching and error handling.
 *
 * Manages loading and error states, automatically refetches
 * when userId changes, and implements stale-while-revalidate caching.
 *
 * @hook
 * @param {string} userId - The ID of the user to fetch
 * @param {Object} options - Hook options
 * @param {number} options.cacheTime - Cache duration in ms (default: 60000)
 * @param {boolean} options.skip - Skip fetching if true (default: false)
 *
 * @returns {Object} User data and loading/error states
 * @returns {User | null} returns.user - User data or null if loading/errored
 * @returns {boolean} returns.loading - Whether data is being fetched
 * @returns {Error | null} returns.error - Error object if fetch failed
 * @returns {() => Promise<void>} returns.refetch - Manual refetch function
 *
 * @example
 * const { user, loading, error, refetch } = useUser("user-123");
 * if (loading) return <Spinner />;
 * if (error) return <Error message={error.message} />;
 * return <UserProfile user={user} onRefresh={refetch} />;
 */
export function useUser(
  userId: string,
  options: { cacheTime?: number; skip?: boolean } = {}
) {
  const [user, setUser] = React.useState<User | null>(null);
  const [loading, setLoading] = React.useState(!options.skip);
  const [error, setError] = React.useState<Error | null>(null);

  const refetch = React.useCallback(async () => {
    setLoading(true);
    try {
      const response = await fetch(`/api/users/${userId}`);
      const data = await response.json();
      setUser(data);
      setError(null);
    } catch (err) {
      setError(err as Error);
    } finally {
      setLoading(false);
    }
  }, [userId]);

  React.useEffect(() => {
    if (!options.skip) {
      refetch();
    }
  }, [userId, options.skip, refetch]);

  return { user, loading, error, refetch };
}
```

---

## Utility Functions

```typescript
/**
 * Formats a date according to the user's locale and timezone.
 *
 * Converts a Date object or ISO string to a human-readable
 * format based on browser locale and timezone settings.
 * Falls back to ISO format if formatting fails.
 *
 * @param {Date | string} date - Date to format
 * @param {Object} options - Formatting options
 * @param {string} options.format - Format type: 'short' | 'long' | 'full' (default: 'short')
 * @param {boolean} options.includeTime - Include time in output (default: false)
 *
 * @returns {string} Formatted date string
 *
 * @example
 * formatDate(new Date(), { format: 'long', includeTime: true })
 * // Output: "January 15, 2024 at 10:30 AM"
 */
export function formatDate(
  date: Date | string,
  options: { format?: "short" | "long" | "full"; includeTime?: boolean } = {}
): string {
  const dateObj = typeof date === "string" ? new Date(date) : date;

  const dateFormatOptions: Intl.DateTimeFormatOptions = {
    month: options.format === "short" ? "numeric" : options.format === "long" ? "long" : "long",
    day: "numeric",
    year: "numeric",
  };

  if (options.includeTime) {
    dateFormatOptions.hour = "numeric";
    dateFormatOptions.minute = "2-digit";
  }

  return new Intl.DateTimeFormat(undefined, dateFormatOptions).format(dateObj);
}
```

---

## Best Practices

### ✓ DO

- Document component props with JSDoc comments
- Specify whether components are Server or Client Components
- Include `@example` blocks showing typical usage
- Document async behavior and side effects
- Explain TypeScript generics clearly
- Document exceptions and error cases
- Use clear, specific parameter descriptions

### ✗ DON'T

- Omit types in JSDoc when using TypeScript
- Document obvious props (e.g., `children: React.ReactNode`)
- Mix Server and Client Component responsibilities without explanation
- Leave unused parameters undocumented
- Use vague terms like "data" or "value" without context

---

## Type Documentation Examples

### Props Interface

```typescript
/**
 * Props for the Button component.
 * Extends HTML button attributes for full compatibility.
 */
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  /** Button display variant */
  variant?: "primary" | "secondary" | "danger";
  /** Button size */
  size?: "sm" | "md" | "lg";
  /** Whether button is disabled */
  isDisabled?: boolean;
  /** Loading state indicator */
  isLoading?: boolean;
  /** Icon to display before text */
  icon?: React.ReactNode;
}
```

### API Response Types

```typescript
/**
 * Standard API response format for all endpoints.
 * @template T The data payload type
 */
interface ApiResponse<T> {
  /** Whether the request was successful */
  success: boolean;
  /** Response data or error details */
  data: T | { message: string; code: string };
  /** Request timestamp for debugging */
  timestamp: string;
}
```

---

## Configuration Documentation

Document environment variables and Next.js config:

```typescript
/**
 * Environment variables required by the application.
 *
 * @env {string} NEXT_PUBLIC_API_URL - Public API base URL
 * @env {string} DATABASE_URL - Private database connection string
 * @env {string} NEXTAUTH_SECRET - Secret for NextAuth.js encryption
 * @env {boolean} DEBUG - Enable debug logging (default: false)
 */
```
