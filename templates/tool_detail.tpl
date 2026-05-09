% rebase('base.tpl', title=tool['name'], user=user)

<div class="tool-detail-wrap">

  <!-- ── Tool header ── -->
  <div class="tool-hero">
    <div class="tool-hero-icon">{{tool['name'][0]}}</div>
    <div class="tool-hero-info">
      <div class="tool-hero-top">
        <span class="badge badge-cat">{{tool['category']}}</span>
        % if tool['price'] == 0:
          <span class="badge badge-free">Free</span>
        % else:
          <span class="badge badge-paid">${{"%.0f" % tool['price']}}/mo</span>
        % end
      </div>
      <h1>{{tool['name']}}</h1>
      <p class="tool-hero-company">by {{tool['company']}}</p>

      <div class="rating-row">
        <div class="stars-lg">
          % r = round(tool['rating'])
          % for i in range(1,6):
            <span class="{{'star filled' if i<=r else 'star'}}">★</span>
          % end
        </div>
        <span class="rating-lg-num">{{tool['rating']}}</span>
        <span class="review-count">({{len(reviews)}} review{{'s' if len(reviews)!=1 else ''}})</span>
      </div>

      % if tags:
        <div class="tag-list">
          % for tag in tags:
            <span class="tag">{{tag['tag']}} <span class="tag-count">{{tag['count']}}</span></span>
          % end
        </div>
      % end
    </div>

    <div class="tool-hero-actions">
      % if user:
        <form method="post" action="/tool/{{tool['ai_ID']}}/bookmark">
          <button type="submit" class="{{'btn-bookmark active' if bookmarked else 'btn-bookmark'}}">
            {{'🔖 Bookmarked' if bookmarked else '🔖 Bookmark'}}
          </button>
        </form>
      % end
    </div>
  </div>

  <!-- ── Topical averages ── -->
  % if avg_topical:
    <div class="topical-avg-bar">
      <h3>Average Ratings by Category</h3>
      <div class="topical-grid">
        % for tr in avg_topical:
          <div class="topical-item">
            <span class="topical-label">{{tr['types'].replace('_',' ').title()}}</span>
            <div class="topical-bar-wrap">
              <div class="topical-bar" style="width:{{'%.0f' % (tr['avg_rating']/5*100)}}%"></div>
            </div>
            <span class="topical-num">{{tr['avg_rating']}}</span>
          </div>
        % end
      </div>
    </div>
  % end

  <div class="detail-columns">

    <!-- ── Reviews ── -->
    <div class="reviews-col">
      <h2 class="section-title">Reviews</h2>

      % if not reviews:
        <div class="empty-state">Be the first to review {{tool['name']}}!</div>
      % end

      % for rev in reviews:
        <div class="review-card">
        % if user and user['user_ID'] == rev['user_ID']:
          <form method="post"
                action="/review/{{rev['review_ID']}}/delete"
                onsubmit="return confirm('Delete this review?');">
            <button type="submit" class="btn-sm">
              Delete Review
            </button>
          </form>
        % end
          <div class="review-header">
            <a href="/profile/{{rev['user_ID']}}" class="reviewer-name">{{rev['username']}}</a>
            <div class="stars-sm">
              % r = round(rev['rating'])
              % for i in range(1,6):
                <span class="{{'star filled' if i<=r else 'star'}}">★</span>
              % end
              <span class="rating-num">{{rev['rating']}}</span>
            </div>
            <span class="review-date">
              % import time as _t
              {{_t.strftime('%b %d, %Y', _t.localtime(rev['date']))}}
            </span>
            % if rev['version'] > 1:
              <span class="badge badge-cat">Edited v{{rev['version']}}</span>
            % end
          </div>

          % if topical.get(rev['review_ID']):
            <div class="topical-chips">
              % for tr in topical[rev['review_ID']]:
                <span class="chip">{{tr['types'].replace('_',' ').title()}} <strong>{{tr['rating']}}</strong></span>
              % end
            </div>
          % end

          % if rev['written_Review']:
            <p class="review-text">{{rev['written_Review']}}</p>
          % end

          <div class="vote-row">
            <span class="vote-label">Helpful?</span>
            % if user:
              <form method="post" action="/review/{{rev['review_ID']}}/vote" class="vote-form">
                <input type="hidden" name="vote" value="1">
                <button type="submit" class="vote-btn up">👍 {{rev['upvotes']}}</button>
              </form>
              <form method="post" action="/review/{{rev['review_ID']}}/vote" class="vote-form">
                <input type="hidden" name="vote" value="-1">
                <button type="submit" class="vote-btn down">👎 {{rev['downvotes']}}</button>
              </form>
            % else:
              <span class="vote-static">👍 {{rev['upvotes']}} &nbsp; 👎 {{rev['downvotes']}}</span>
            % end
          </div>
        </div>
      % end
    </div>

    <!-- ── Write / Edit Review ── -->
    <div class="review-form-col">
      % if user:
        <div class="review-form-box">
          <h3>{{'Edit your review' if user_review else 'Write a review'}}</h3>
          <form method="post" action="/tool/{{tool['ai_ID']}}/review">

            <label>Overall Rating</label>
            <div class="star-picker" id="star-picker">
              % cur_r = user_review['rating'] if user_review else 0
              % for i in range(1,6):
                <span class="star-pick {{'filled' if i<=cur_r else ''}}" data-val="{{i}}">★</span>
              % end
              <input type="hidden" name="rating" id="rating-input" value="{{int(cur_r) if user_review else 3}}">
            </div>

            <label>Written Review <span class="opt">(optional)</span></label>
            <textarea name="written_review" rows="4" placeholder="Share your experience…">{{user_review['written_Review'] if user_review else ''}}</textarea>

            <label style="margin-top:1rem">Category Ratings <span class="opt">(optional)</span></label>
            % topical_types = [('ease_of_use','Ease of Use'),('accuracy','Accuracy'),('value','Value for Money'),('creativity','Creativity'),('support','Support')]
            % for tkey, tlabel in topical_types:
              <div class="topical-input-row">
                <span class="topical-input-label">{{tlabel}}</span>
                <select name="topical_{{tkey}}">
                  <option value="">—</option>
                  % for v in ['1','2','3','4','5']:
                    <option value="{{v}}">{{v}} ★</option>
                  % end
                </select>
              </div>
            % end

            <button type="submit" class="btn-primary" style="margin-top:1.2rem;width:100%">
              {{'Update Review' if user_review else 'Submit Review'}}
            </button> 
          </form>
        </div>
      % else:
        <div class="review-form-box login-prompt">
          <p><a href="/login">Log in</a> or <a href="/register">sign up</a> to leave a review.</p>
        </div>
      % end
    </div>

  </div><!-- end detail-columns -->
</div>
