% rebase('base.tpl', title=profile_user['username'], user=current_user)
% import time as _t

<div class="profile-wrap">
  <div class="profile-header">
    <div class="profile-avatar">{{profile_user['username'][0].upper()}}</div>
    <div class="profile-info">
      <h1>{{profile_user['username']}}</h1>
      <p class="profile-meta">
        &nbsp;Member since {{_t.strftime('%b %Y', _t.localtime(profile_user['date_Created']))}}
      </p>
      <p class="profile-stats">
        <strong>{{len(reviews)}}</strong> review{{'s' if len(reviews)!=1 else ''}}
      </p>
    </div>
  </div>

  <h2 class="section-title">Reviews by {{profile_user['username']}}</h2>

  % if not reviews:
    <div class="empty-state">No reviews yet.</div>
  % end

  % for rev in reviews:
    <div class="review-card">
      <div class="review-header">
        <a href="/tool/{{rev['ai_ID']}}" class="reviewer-name">{{rev['tool_name']}}</a>
        <div class="stars-sm">
          % r = round(rev['rating'])
          % for i in range(1,6):
            <span class="{{'star filled' if i<=r else 'star'}}">★</span>
          % end
          <span class="rating-num">{{rev['rating']}}</span>
        </div>
        <span class="review-date">{{_t.strftime('%b %d, %Y', _t.localtime(rev['date']))}}</span>
      </div>
      % if rev['written_Review']:
        <p class="review-text">{{rev['written_Review']}}</p>
      % end
    </div>
  % end

  % if current_user and current_user['user_ID'] == profile_user['user_ID'] and bookmarks:
    <h2 class="section-title" style="margin-top:2.5rem">Your Bookmarks</h2>
    <div class="tool-grid">
      % for tool in bookmarks:
        <a class="tool-card" href="/tool/{{tool['ai_ID']}}"
          <div class="tool-icon">{{tool['name'][0]}}</div>
          <h3 class="tool-name">{{tool['name']}}</h3>
          <p class="tool-company">{{tool['company']}}</p>
          <div class="stars-sm">
            % r = round(tool['rating'])
            % for i in range(1,6):
              <span class="{{'star filled' if i<=r else 'star'}}">★</span>
            % end
          </div>
        </a>
      % end
    </div>
  % end
</div>
