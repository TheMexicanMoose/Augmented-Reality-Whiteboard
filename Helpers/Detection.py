
def check_overlap(l1, r1, l2, r2):
    if l1[0] > r2[0] or l2[0] > r1[0]:
        return False

    if l1[1] > r2[1] or l2[1] > r1[1]:
        return False

    return True

def get_overlap_cords(l1, r1, l2, r2):
    new_x1 = max(l1[0], l2[0])
    new_y1 = max(l1[1], l2[1])
    new_x2 = min(r2[0], r1[0])
    new_y2 = min(r1[1], r2[1])

    return [new_x1, new_y1, new_x2, new_y2]

def get_middle(x1, y1, x2, y2):
    middle_x = (x1 + x2) / 2
    middle_y = (y1 + y2) / 2
    return [middle_x, middle_y]

