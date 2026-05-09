% rebase('base.tpl', title='Submit a Tool', user=user)

<div class="auth-wrap">
  <div class="auth-box" style="max-width:560px">
    <h2>Submit an AI Tool</h2>
    <p class="auth-sub">Know a great AI tool that's not listed? Add it for the community.</p>

    % if defined('error') and error:
      <div class="alert alert-error">{{error}}</div>
    % end

    <form method="post" action="/add-tool">
      <label>Tool Name *</label>
      <input type="text" name="name" required placeholder="e.g. Stable Diffusion">

      <label>Company / Creator *</label>
      <input type="text" name="company" required placeholder="e.g. Stability AI">

      <label>Category *</label>
      <select name="category" required>
        <option value="">Select a category…</option>
        % for cat in categories:
          <option value="{{cat}}">{{cat}}</option>
        % end
      </select>

      <label>Price (USD/month, 0 = free)</label>
      <input type="number" name="price" value="0" min="0" step="0.01">

      <button type="submit" class="btn-primary" style="width:100%;margin-top:1.2rem">Submit Tool</button>
    </form>
  </div>
</div>
