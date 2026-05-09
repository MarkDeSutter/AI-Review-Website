% rebase('base.tpl', title='Search', user=user, search_q=q)

<div class="page-wrap">
  <aside class="sidebar">
    <h3>Filter</h3>
    <form method="get" action="/search" id="filter-form">
      <input type="hidden" name="q" value="{{q}}">

      <label class="filter-label">Category</label>
      % for cat in categories:
        <label class="check-label">
          <input type="radio" name="category" value="{{cat['category']}}"
            {{'checked' if selected_category == cat['category'] else ''}}>
          {{cat['category']}}
        </label>
      % end
      <label class="check-label">
        <input type="radio" name="category" value="" {{'checked' if not selected_category else ''}}>
        All categories
      </label>

      <label class="filter-label" style="margin-top:1.2rem">Sort by</label>
      <select name="sort" onchange="document.getElementById('filter-form').submit()">
        <option value="rating" {{'selected' if sort=='rating' else ''}}>Top Rated</option>
        <option value="name"   {{'selected' if sort=='name'   else ''}}>Name A–Z</option>
        <option value="price"  {{'selected' if sort=='price'  else ''}}>Price: Low–High</option>
      </select>

      <button type="submit" class="btn-sm" style="margin-top:1rem;width:100%">Apply</button>
    </form>
  </aside>

  <div class="results">
    <div class="results-header">
      <h2>
        % if q:
          Results for "{{q}}"
        % elif selected_category:
          {{selected_category}}
        % else:
          All AI Tools
        % end
      </h2>
      <span class="result-count">{{len(tools)}} tool{{'s' if len(tools)!=1 else ''}}</span>
    </div>

    % if not tools:
      <div class="empty-state">
        <p>No tools match your search. <a href="/add-tool">Submit one?</a></p>
      </div>
    % end

    <div class="tool-list">
      % for tool in tools:
        <a class="tool-row" href="/tool/{{tool['ai_ID']}}">
          <div class="tool-row-icon">{{tool['name'][0]}}</div>
          <div class="tool-row-body">
            <div class="tool-row-top">
              <h3>{{tool['name']}}</h3>
              <span class="badge badge-cat">{{tool['category']}}</span>
            </div>
            <p class="tool-company">{{tool['company']}}</p>
          </div>
          <div class="tool-row-right">
            <div class="stars-sm">
              % r = round(tool['rating'])
              % for i in range(1,6):
                <span class="{{'star filled' if i<=r else 'star'}}">★</span>
              % end
            </div>
            <span class="rating-big">{{tool['rating']}}</span>
            % if tool['price'] == 0:
              <span class="badge badge-free">Free</span>
            % else:
              <span class="badge badge-paid">${{"%.0f" % tool['price']}}/mo</span>
            % end
          </div>
        </a>
      % end
    </div>
  </div>
</div>
