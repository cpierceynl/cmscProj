
class htmlReportGenerator():
    def __init__(self, img1, img2, img3, df, img4):
        """set attributes
        title
        description
        """
        self.report_title = "Sea Ice Concentration Analysis"
        self.report_text = "Comparison: Sea ice concentration in %, 1980 and 2022"
        self.df = df  # predictions data
        self.img1 = img1  # heatmap of 1980s
        self.img2 = img2  # heatmap 2021
        self.report_text2 = "Average concentration, 1980-2022"
        self.report_text3 = "Prediction concentration heatmap"
        self.df_text = "Predicted values"
        self.img3 = img3  # averages
        self.img4 = img4  # predicted heatmap

    def make_report(self):
        html = f'''
            <html>
                <head>
                    <title>'Ice Concentration: Report'</title>
                </head>
                <body>
                    <h1>{self.report_title}</h1>
                    <p>{self.report_text}</p>
                    <img src={self.img1}>
                    
                    <img src={self.img2}>
                    <p>{self.report_text2}</p>
                    <img src={self.img3}>
                    <p>{self.df_text}</p>
                    {self.df.to_html()}
                    <p>{self.report_text3}</p>
                    <img src={self.img4}>
                </body>
            </html>
        '''

        with open(r'C:\Users\Caitlin\Desktop\prediction_report_demo.html', 'w') as file:
            file.write(html)

        return


