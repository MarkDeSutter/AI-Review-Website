% rebase('base.tpl', title='Log In')

<div class="auth-wrap">
  <div class="auth-box">
    <h2>Welcome back</h2>
    <p class="auth-sub">Log in to ToolRank to continue reviewing AI tools.</p>

    % if defined('error') and error:
      <div class="alert alert-error">{{error}}</div>
    % end

    <form method="post" action="/login">
      <label>Username</label>
      <input type="text" name="username" required autocomplete="username" placeholder="Your username">

      <label>Password</label>
      <input type="password" name="password" required autocomplete="current-password" placeholder="Your password">

      <button type="submit" class="btn-primary" style="width:100%;margin-top:1.2rem">Log In</button>
    </form>

    <p class="auth-switch">Don't have an account? <a href="/register">Sign up free</a></p>
  </div>
</div>
