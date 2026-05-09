% rebase('base.tpl', title='Sign Up')

<div class="auth-wrap">
  <div class="auth-box">
    <h2>Create your account</h2>
    <p class="auth-sub">Join ToolRank to review AI tools and save your favorites.</p>

    % if defined('error') and error:
      <div class="alert alert-error">{{error}}</div>
    % end

    <form method="post" action="/register">
      <label>Username</label>
      <input type="text" name="username" required autocomplete="username" placeholder="e.g. janedoe42">

      <label>Email</label>
      <input type="email" name="email" required autocomplete="email" placeholder="you@example.com">

      <label>Password</label>
      <input type="password" name="password" required autocomplete="new-password" placeholder="At least 8 characters">

      <button type="submit" class="btn-primary" style="width:100%;margin-top:1.4rem">Create Account</button>
    </form>

    <p class="auth-switch">Already have an account? <a href="/login">Log in</a></p>
  </div>
</div>
