import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cpf

class visualizeConcentration():
    """
    visualizeConcentration class produces formatted matplotlib plots
    """
    def __init__(self, df, sp, year):
        """
        initialize object attributes
        """
        self.df = df
        self.sp = sp
        self.x = df['lon']
        self.y = df['lat']
        self.z = df['concentration']
        self.year = year


    def draw_fig(self):
        # initialize figure
        x = self.df['lon']
        y = self.df['lat']
        z = self.df['concentration']

        self.m = plt.subplot(projection=ccrs.NorthPolarStereo())

        # add labels, change size, etc
        self.m.gridlines(draw_labels=True, zorder=13)
        self.m.set_global()  # visualize entire globe

        # zoom into arctic region (above 60 degrees N)
        self.m.set_extent([-180, 180, 60, 90], crs=ccrs.PlateCarree())
        # add features from cartopy, set on top of heatmap
        self.m.add_feature(cpf.COASTLINE, zorder=12)
        self.m.add_feature(cpf.LAND, zorder=11)

        spacing = 50  # reduce spacing to 50 for runtime purposes
        xi, yi = np.linspace(x.min(), x.max(), spacing), np.linspace(y.min(), y.max(), spacing)

        XI, YI = np.meshgrid(xi, yi)  # create coordinate matrix

        from scipy.interpolate import griddata

        # interpolate between points
        ZI = griddata((x, y), z, (XI, YI), method='linear')

        # create heatmap of region with concentration as data, set under features
        heatmap = self.m.pcolormesh(XI, YI, ZI, zorder=10, transform=ccrs.PlateCarree())
        plt.colorbar(heatmap, orientation='horizontal')
        plt.title("Ice concentration: " + str(self.year))

        plt.savefig('figure' + str(self.sp) + '.png')
        return(heatmap)

    def trend_fig(self):
        x = self.df['year']
        y = self.df['concentration']

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)

        # add trendline to plot
        trend = plt.plot(x, p(x), color='green', linestyle='--', label='Trendline')
        plt.scatter(x,y, color='blue', label='Measured data')
        plt.xlabel("Year")
        plt.ylabel("Concentration (mean,%)")
        plt.title("Average ice concentration from 1980-2021")
        plt.legend()
        plt.savefig('averages.png')
        return(trend)
