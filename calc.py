import math

class Calc:
    @staticmethod
    def closest_point_on_line(lx1, ly1, lx2, ly2, x0, y0):
        A1 = ly2 - ly1
        B1 = lx1 - lx2
        C1 = (ly2 - ly1) * lx1 + (lx1 - lx2) * ly1
        C2 = -B1 * x0 + A1 * y0
        det = A1 * A1 - (-B1) * B1
        if det != 0:
            cx = (A1 * C1 - B1 * C2) / det
            cy = (A1 * C2 - (-B1) * C1) / det
        else:
            cx = x0
            cy = y0
        return (cx, cy)

    @staticmethod
    def distance(point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

    @staticmethod
    def reflect_vector(bx, by, vx, vy, cx, cy):
        # Calculate the collision distance
        collision_dist = math.sqrt((bx - cx) ** 2 + (by - cy) ** 2)
        
        # Calculate the normal vector (n_x, n_y)
        n_x = (bx - cx) / collision_dist
        n_y = (by - cy) / collision_dist
        
        # Calculate the dot product
        dot_product = vx * n_x + vy * n_y
        
        # Calculate the reflection vector (new velocity vector)
        w_x = vx - 2 * dot_product * n_x
        w_y = vy - 2 * dot_product * n_y
        
        return w_x, w_y