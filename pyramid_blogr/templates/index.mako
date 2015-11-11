<%inherit file="pyramid_blogr:templates/layout.mako"/>
<% link_attr={"class": "btn btn-default btn-xs"} %>
<% curpage_attr={"class": "btn btn-default btn-xs disabled"} %>
<% dotdot_attr={"class": "btn btn-default btn-xs disabled"} %>

% if request.authenticated_userid:
    Welcome <strong>${request.authenticated_userid}</strong> ::
    <a href="${request.route_url('auth',action='out')}">Sign Out</a>
%else:
    <form action="${request.route_url('auth',action='in')}" method="post" class="form-inline">
        <div class="form-group">
            <label>User</label> <input type="text" name="username" class="form-control">
        </div>
        <div class="form-group">
        <label>Password</label> <input type="password" name="password" class="form-control">
        <input type="submit" value="Sign in" class="btn btn-default">
        </div>
    </form>
    <a href="${request.route_url('register')}">Register here</a>
%endif

% if paginator.items:

    <h2>Blog entries</h2>

    <ul>
        % for entry in paginator.items:
            <li>
                <a href="${request.route_url('blog', id=entry.id, slug=entry.slug)}">
                    ${entry.title}</a>
            </li>
        % endfor
    </ul>

    ${paginator.pager(link_attr=link_attr, curpage_attr=curpage_attr, dotdot_attr=dotdot_attr) |n}

% else:

    <p>No blog entries found.</p>

%endif

<p><a href="${request.route_url('blog_action',action='create')}">
    Create a new blog entry</a></p>