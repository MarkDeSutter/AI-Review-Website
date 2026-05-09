<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{get('title', 'ToolRank') }} — AI Tool Reviews</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>

<nav class="navbar">
  <a class="nav-brand" href="/">Tool<span>Rank</span></a>

  <form class="nav-search" action="/search" method="get">
    <input type="text" name="q" placeholder="Search AI tools…" value="{{get('search_q','')}}">
    <button type="submit">⌕</button>
  </form>

  <div class="nav-links">
    % if defined('user') and user:
      <a href="/profile/{{user['user_ID']}}">{{user['username']}}</a>
      <a href="/add-tool" class="btn-sm">+ Submit Tool</a>
      <a href="/logout" class="btn-sm btn-ghost">Log out</a>
    % else:
      <a href="/login">Log in</a>
      <a href="/register" class="btn-sm">Sign up</a>
    % end
  </div>
</nav>

<main>
  {{!base}}
</main>

<footer>
  <p>ToolRank &mdash; A Databases Final Project &bull; Built with Python Bottle + PostgreSQL</p>
</footer>

<script src="/static/js/main.js"></script>
</body>
</html>
