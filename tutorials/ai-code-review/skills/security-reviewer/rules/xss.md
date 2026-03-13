# Cross-Site Scripting (XSS)

## Priority: CRITICAL

## Description

XSS occurs when user input is rendered as HTML without sanitization. Attackers can inject scripts that steal cookies, redirect users, or modify page content.

## Vulnerable

```javascript
// React: dangerouslySetInnerHTML with user input
<div dangerouslySetInnerHTML={{ __html: userComment }} />

// Direct DOM manipulation
element.innerHTML = userInput;
document.write(userData);
```

```python
# Flask/Jinja2: Markup() or |safe with user input
return Markup(f"<p>{user_comment}</p>")

# Django: mark_safe with user input
return mark_safe(f"<div>{user_input}</div>")
```

## Fixed

```javascript
// React: render as text (default behavior is safe)
<div>{userComment}</div>

// If HTML is needed, sanitize first
import DOMPurify from "dompurify";
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userComment) }} />
```

```python
# Let the template engine auto-escape (default in Jinja2/Django)
return render_template("page.html", comment=user_comment)
```

## What to Check

- `dangerouslySetInnerHTML` with any variable that could contain user input
- `.innerHTML` assignments with user data
- `Markup()`, `mark_safe()`, `|safe` filter with user data
- URL parameters rendered without escaping
- User input in `href`, `src`, or event handler attributes
