from collections import defaultdict
from heapq import *

def dijkstra(edges,start, stop):
    # słownik użyty w celu łatwiejszego zarządzania węzłami
    dict = defaultdict(list)
    # uzupełnianie słownika
    for l_node,r_node,cost in edges:
        dict[l_node].append((cost, r_node))
        dict[r_node].append((cost, l_node))
    # utworzenie kolejki priorytetowej poprzez wprowadzenie węzła startowego
    priorityq = [(0,start,())]
    # lista węzłów, które zostały odwiedzone
    seen = set()
    while priorityq:
        print(priorityq)
        # zwraca i usuwa najmniejszy element kopca utrzymująć jego założenia
        (cost,v1,path) = heappop(priorityq)
        # jeśli węzeł nie był jeszcze odwiedzony
        if v1 not in seen:
            # dodanie węzła do listy węzłów odwiedzonych
            seen.add(v1)
            # aktualizacja ścieżki
            path += (v1, )
            # jeśli rozważany węzeł jest wybranym ostatnim węzłem w ścieżce to algorytm
            # kończy się i zostaje zwrócona znaleciona ścieżka
            if v1 == stop: return path

            # dla każdego węzła, który sąsiaduje z obecnie rozważanym (v1)
            for cost_next, v_next in dict.get(v1, ()):
                # jeśli węzeł był już odwiedzony to nie rób nic
                if v_next in seen: continue
                # w przeciwnym wypadku rozszerz kolejkę priorytetową (zachowując właściwości kopca)
                # o węzeł (v_next) dla którego koszt dojścia jest sumą kosztów dojścia do węzła go
                # poprzedzającego (v1) i kosztem od węzła poprzedzającego dotego węzła (cost + cost_next)
                heappush(priorityq, (cost + cost_next, v_next, path))
    # zwróć nieskończoność jeśli nie ma możliwości wyznaczenia trasy
    return float("inf")


if __name__ == "__main__":
    edges = [
        ("A", "B", 7),
        ("A", "D", 5),
        ("B", "C", 8),
        ("B", "D", 9),
        ("B", "E", 7),
        ("C", "E", 5),
        ("D", "E", 15),
        ("D", "F", 6),
        ("E", "F", 8),
        ("E", "G", 9),
        ("F", "G", 11)
    ]
    edges2 =[("a", "b", 7), ("a", "c", 9),("a", "f", 14), ("b", "c", 10), ("b", "d", 15), ("c", "d", 11), ("c", "f", 2), ("d", "e", 6),("e", "f", 9)]

    print(dijkstra(edges2, "a", "f"))