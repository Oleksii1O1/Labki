def solve_gamsrv(n, m, clients, edges):

    graph = {i: [] for i in range(1, n + 1)}
    for u, v, latency in edges:
        graph[u].append((v, latency))
        graph[v].append((u, latency))

    min_max_latency = float("inf")
    client_set = set(clients)

    for server_candidate in range(1, n + 1):
        if server_candidate in client_set:
            continue


        distances = [float("inf")] * (n + 1)
        visited = [False] * (n + 1)
        distances[server_candidate] = 0
        
        max_latency_for_this_server = 0
        visited_clients_count = 0


        for _ in range(n):

            current_node = -1
            min_dist = float("inf")
            for i in range(1, n + 1):
                if not visited[i] and distances[i] < min_dist:
                    min_dist = distances[i]
                    current_node = i

  
            if current_node == -1:
                break

            visited[current_node] = True

            # Якщо це клієнт, оновлюємо максимальну затримку
            if current_node in client_set:
                if distances[current_node] > max_latency_for_this_server:
                    max_latency_for_this_server = distances[current_node]
                visited_clients_count += 1

            # Релаксація ребер
            for neighbor, weight in graph[current_node]:
                new_dist = distances[current_node] + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist

        # Перевіряємо, чи всі клієнти досяжні
        if visited_clients_count == len(clients):
            if max_latency_for_this_server < min_max_latency:
                min_max_latency = max_latency_for_this_server

    return min_max_latency


def main():
    try:
        with open("gamsrv_in.txt", "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        if not lines:
            return

        n, m = map(int, lines[0].split())
        clients = list(map(int, lines[1].split()))

        edges = []
        for i in range(2, m + 2):
            u, v, latency = map(int, lines[i].split())
            edges.append((u, v, latency))

        result = solve_gamsrv(n, m, clients, edges)

        with open("gamsrv_out.txt", "w") as f:
            f.write(str(result) + "\n")

    except FileNotFoundError:
        pass


if __name__ == "__main__":
    main()