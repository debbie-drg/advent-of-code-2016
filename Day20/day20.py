import sys


class IPRange:
    def __init__(self, extremes: list[int]):
        self.extremes = extremes

    def __repr__(self) -> str:
        return f"[{self.extremes[0]}, {self.extremes[1]}]"

    def __len__(self):
        if self.extremes == []:
            return 0
        return self.extremes[1] - self.extremes[0] + 1

    def contains(self, element: int):
        return self.extremes[0] <= element and element <= self.extremes[1]

    def intersects(self, __o):
        return self.contains(__o.extremes[0]) or self.contains(__o.extremes[1])

    def contiguous(self, __o):
        return self.extremes[1] == __o.extremes[0] - 1

    def union(self, __o):
        self.extremes[0] = min(self.extremes[0], __o.extremes[0])
        self.extremes[1] = max(self.extremes[1], __o.extremes[1])


class IPRanges:
    def __init__(self, intervals: list[IPRange]):
        self.intervals = intervals

    def __repr__(self) -> str:
        return f"Intervals: {self.intervals}"

    def __len__(self):
        self.merge()
        return sum(len(interval) for interval in self.intervals)

    def add(self, interval: IPRange):
        if interval.extremes == []:
            return None
        self.intervals.append(interval)
        self.merge()

    def merge_contiguous(self):
        self.intervals.sort(key=lambda x: x.extremes[0])
        index = 0
        while index < len(self.intervals) - 1:
            if self.intervals[index].contiguous(self.intervals[index + 1]):
                self.intervals[index].extremes[1] = self.intervals[index + 1].extremes[
                    1
                ]
                self.intervals.pop(index + 1)
            else:
                index += 1

    def merge(self):
        self.intervals.sort(key=lambda x: x.extremes[0])
        while True:
            checked_until = 0
            changed = False
            for index in range(checked_until, len(self.intervals) - 1):
                if self.intervals[index].intersects(self.intervals[index + 1]):
                    self.intervals[index].union(self.intervals[index + 1])
                    self.intervals.pop(index + 1)
                    changed = True
                    checked_until = index
                    break
            if not changed:
                break
        self.merge_contiguous()

    def first_free_ip(self):
        self.merge()
        if self.intervals[0].extremes[0] != 0:
            return 0
        return self.intervals[0].extremes[1] + 1

    def allowed_ips(self, max_range: int):
        self.merge()
        count = 0
        for index in range(len(self.intervals) - 1):
            count += (
                self.intervals[index + 1].extremes[0]
                - self.intervals[index].extremes[1]
            ) - 1
        count += max_range - self.intervals[-1].extremes[1]
        return count


def create_intervals(input_data: list[str]) -> IPRanges:
    interval_list = []
    for element in input_data:
        interval_list.append(IPRange([int(extreme) for extreme in element.split("-")]))
    return IPRanges(interval_list)


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    max_range = 9 if "example" in file_name else 4294967295
    data = open(file_name).read().strip().split("\n")
    ipranges = create_intervals(data)
    print(f"The first free IP is {ipranges.first_free_ip()}")
    print(f"The number of allowed IPs is {ipranges.allowed_ips(max_range)}")
