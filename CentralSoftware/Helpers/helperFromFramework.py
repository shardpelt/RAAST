class Helper:
    @staticmethod
    def is_between_angles(n, alpha, beta) -> float:
        if alpha < beta:
            return alpha <= n <= beta
        return alpha <= n or n <= beta

    @staticmethod
    def distance_between_angles(alpha, beta) -> float:
        phi = abs(beta - alpha) % 360
        distance = (180 - phi) % 360 if phi > 90 else phi
        return distance
