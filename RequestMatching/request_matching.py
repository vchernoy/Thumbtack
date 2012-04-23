# Author: Viacheslav CHernoy
# Email: vchernoy@gmail.com
# 
# The solution of Problem 4: Request Matching
# See http://www.thumbtack.com/challenges

def new_vertex(graph):
    graph.append([])
    return len(graph) - 1

def add_edge(graph, v, u):
    assert(u not in graph[v])
    graph[v].append(u)

def remove_edge(graph, v, u):
    assert(u in graph[v])
    graph[v].remove(u)


def dfs(graph, src, dst):
    predecessor = [None] * len(graph)
    
    assert(src != dst)

    stack = [src]
    predecessor[src] = -1
    while stack and (predecessor[dst] == None):
        v = stack.pop()
        for u in graph[v]:
            if predecessor[u] == None:
                stack.append(u)
                predecessor[u] = v
                if u == dst:
                    break

    path = []
    if predecessor[dst] != None:
        v = dst
        while v != src:
            path.insert(0, v)
            v = predecessor[v]

        path.insert(0, src)
        
    return path

def ford_fulkerson_flow(graph, src, dst):
    flow_val = 0
    path = dfs(graph, src, dst)
    while path:
        flow_val += 1
        for i in xrange(1, len(path)):
            remove_edge(graph, path[i-1], path[i])
            add_edge(graph, path[i], path[i-1])

        path = dfs(graph, src, dst)
        
    return flow_val


def flow_problem(services, requests):
    end_time = max([r[2] for r in requests.itervalues()])
    graph = []
    src = new_vertex(graph)

    categories = {}
    for (serv_name, serv_categories) in services.iteritems():
        for cat_name in serv_categories:
            categories.setdefault(cat_name, []).append(serv_name)

    service_vertexes = []
    for t in xrange(1, end_time+1):
        time_services = {}
        for (req_name, req) in requests.iteritems():
            req_cat, beg, end, req_vertexes = req
            if (t >= beg) and (t <= end):
                req_v = new_vertex(graph)
                req_vertexes.append(req_v)
                for serv_name in categories[req_cat]:
                    serv_v = time_services.get(serv_name, -1)
                    if serv_v == -1:
                        serv_v = new_vertex(graph)
                        time_services[serv_name] = serv_v

                    add_edge(graph, serv_v, req_v)

        service_vertexes.extend(time_services.itervalues())

    for serv_v in service_vertexes:
        add_edge(graph, src, serv_v)

    request_vertexes = []

    for req in requests.itervalues():
        req_cat, beg, end, req_vertexes = req
        assert(len(req_vertexes) == end - beg + 1)

        if len(req_vertexes) == 1:
            request_vertexes.append(req_vertexes[0])
        else:
            common_req_vert = new_vertex(graph)
            request_vertexes.append(common_req_vert)
            for req_vert in req_vertexes:
                add_edge(graph, req_vert, common_req_vert)

    dst = new_vertex(graph)
    for req_v in request_vertexes:
        add_edge(graph, req_v, dst)

    return (graph, src, dst)


def max_matching(services, requests):
    graph, src, dst = flow_problem(services, requests)

    return ford_fulkerson_flow(graph, src, dst)

def main():
    services = {}
    requests = {}
    while True:
        try:
            tokens = raw_input().strip().split()
        except EOFError:
            print max_matching(services, requests)
            break

        if not tokens:
            print max_matching(services, requests)
            services = {}
            requests = {}
        elif tokens[0] == 'service':
            service, categories = tokens[1], tokens[2:]
            services[service] = categories
        elif tokens[0] == 'request':
            request, category, days = tokens[1], tokens[2], [int(w) for w in tokens[3].split('-')]
            beg, end = days[0], days[-1]
            requests[request] = (category, beg, end, [])
        else:
            print "Error"
            assert(False)

if __name__ == '__main__':
    main()
