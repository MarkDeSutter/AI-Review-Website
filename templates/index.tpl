% rebase('base.tpl', title='Home', user=user)

<section class="hero">
  <div class="hero-inner">
    <h1>Find the <em>right</em><br>AI tool for you.</h1>
    <p class="hero-sub">Honest reviews from real users — ranked by ease of use, accuracy, value, and more.</p>
    <form class="hero-search" action="/search" method="get">
      <input type="text" name="q" placeholder="Try 'code assistant' or 'image generation'…">
      <button type="submit">Search</button>
    </form>
    <div class="hero-cats">
      % for cat in categories:
        <a href="/search?category={{cat['category']}}">{{cat['category']}}</a>
      % end
    </div>
  </div>
</section>

<section class="section">
  <div class="section-header">
    <h2>Top Rated Tools</h2>
    <a href="/search?sort=rating">View all →</a>
  </div>
  <div class="tool-grid">
    % for tool in top_tools:
      <a class="tool-card" href="/tool/{{tool['ai_ID']}}">
        <div class="tool-card-top">
          <div class="tool-icon">
            % if tool.get('img_url'):
              <img src="{{tool['img_url']}}" alt="{{tool['name']}}">
            % else:
              {{tool['name'][0]}}
            % end
          </div>
          <div class="tool-meta">
            <span class="tool-category">{{tool['category']}}</span>
            <div class="stars" data-rating="{{tool['rating']}}">
              % r = round(tool['rating'])
              % for i in range(1,6):
                <span class="{{'star filled' if i <= r else 'star'}}">★</span>
              % end
              <span class="rating-num">{{tool['rating']}}</span>
            </div>
          </div>
        </div>
        <h3 class="tool-name">{{tool['name']}}</h3>
        <p class="tool-company">{{tool['company']}}</p>
        <div class="tool-price">
          % if tool['price'] == 0:
            <span class="badge badge-free">Free</span>
          % else:
            <span class="badge badge-paid">${{"%.0f" % tool['price']}}/mo</span>
          % end
        </div>
      </a>
    % end
  </div>
</section>

<section class="cta-band">
  <div class="cta-inner">
    <h2>Have you used an AI tool?</h2>
    <p>Your review helps others find the best tools for their needs.</p>
    % if user:
      <a href="/search" class="btn-lg">Browse &amp; Review</a>
    % else:
      <a href="/register" class="btn-lg">Create a free account</a>
    % end
  </div>
</section>
