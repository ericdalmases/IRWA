# Tweet Data Analysis in Google Colab

This repository contains Python code for analyzing tweet data in a Google Collab notebook. To execute the code successfully, ensure you input your path and have all the important documents in the specified location.

**Execution Steps**

1. **Open Google Colab:**
    - Visit [Google Colab](https://colab.research.google.com/).
2. **Open the notebook provided in the repository**
3. **Input Your Path:**
    - Replace the default path in the code with the path to your specific data location, as well as the destination path for saving the images. Modify the following lines to reflect your path:
        
        data_path = '/content/drive/…’
        
        plt.savefig("/content/drive/…/WordCloud1.jpg")
        
        plt.savefig("/content/drive/…/WordCloud2.jpg")
        
        …
        
        plt.savefig("/content/drive/…/tokernsxtweet.jpg", bbox_inches='tight')
        
        …
        
4. **Mount Google Drive:**
    - Run the first code cell in your notebook to mount your Google Drive.
5. **Execute Code Cells:**
    - Execute each code cell sequentially by clicking the "Run" button or using the keyboard shortcut Shift + Enter.
6. **Visualization Output:**
    - Visualizations, such as word clouds and graphs, will be displayed within the notebook as specified in the code.
7. **Accessing Results:**
    - Any generated files or data will be saved in your Google Drive and displayed within the notebook.

By following these steps, you can run the provided code for tweet data analysis in Google Colab with your specific path and data documents.
