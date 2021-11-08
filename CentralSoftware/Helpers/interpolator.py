class Interpolator:

    @staticmethod
    def getSail(windToSail1, windToSail2, wind):
        deltaX = windToSail2["wind"] - windToSail1["wind"]
        deltaY = windToSail2["sail"] - windToSail1["sail"]
        helling = deltaY / deltaX

        b = windToSail1["sail"] - (helling * windToSail1["wind"])

        y = helling * wind + b
        return y