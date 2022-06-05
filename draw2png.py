from PIL import Image

"""
    draw2png is designed to be a tool to assist artists in turning scanned line 
    art into transparent pngs for use as a layer in digital art software.
    
    Input file must be places in .\input directory. All files will be exported to the .\output directory.
"""

class draw2png:
    def __init__(self, filename, threshold=600, blackout=200, contrast=4):
        """
            threshold:
                integer between 0 and 765, inclusive.
                An upper limit on the intensity of pixes included in the exported image. Anything brighter
                will be set as transparent.
                Set to 765 to disable this feature. Unless contrast is set to 2 (see below), disabling this will result in
                a non-transparent PNG.
                
                Intensity is calculated as the sum of the RBG values for a given pixel.
            blackout:
                integer between 0 and 765, inclusive.
                Any pixel with an intensity (see "threshold" above) below this value will be set to RGB (0,0,0) for crisper images.
                Set to 0 to disable this.
            contrast:
                0: No color alteration is performed. Any pixel brighter than the threshold is kept as-is.
                1: Pixels between the blackout and threshold levels will be made grey, any below the blackout level will be set to black.
                2: All pixels will be set to black, but with a transparency equal to their brightness. EXPERIMENTAL
                3: All pixels below the threshold will be set to black.
        """
        # Set parameter attributes
        self.imagefile = filename
        self.threshold = threshold
        self.blackout = blackout
        self.contrast = contrast
        
        # Import image data from file
        inpath = '.\\input\\'+self.imagefile
        img = Image.open(inpath)
        self.image = img.convert("RGBA")
        self.image_data = self.image.getdata()
        
        # Set default filename for export
        self.saveas = '.\\output\\'+self.imagefile[:-4] + ".png"
        
    def set_saveas(self, saveas):
        self.saveas = saveas
        
        
    def export_png(self):
        print('Processing ', self.imagefile)
        newData = []
        # intensities = []
        for item in self.image_data:
            # Caluculate the pixel intensity as the sum of RGB values
            intensity = item[0] + item[1] + item[2]

            # Any pixel brighter than the intensity is ALWAYS excluded
            if intensity > self.threshold:
                newData.append((0, 0, 0, 0)) # Set pixel as 100% transparent
            else:
                # If it's high contrast, then we don't need to check how close the the 
                # threshold it is
                if self.contrast == 3:
                    newData.append((0, 0, 0, 255)) # Set pixel as 100% opaque
                
                # EXPERIMENTAL: sets the opacity of a pixel equal to its average brightness
                elif self.contrast == 2:
                    # 765 would be a white pixel. Subtracting the brightness from that 
                    # gives us a darkness value.
                    opacity = 765 - (intensity//3 + 1)
                    # Set the pixel color to black, and opaciuty equal to the darkness.
                    newData.append((0, 0, 0, opacity))
                
                # EXPERIMENTAL: sets each pixel between the blackout level and threshold 
                #               to a grey with equivalent brightness
                elif self.contrast == 1: #(c-a)*(b-c) >= 0: check if c is between a and b
                    if (intensity - self.blackout) * (self.threshold - intensity) >= 0:
                        grey = intensity//3 + 1
                        newData.append((grey, grey, grey, 255))
                    elif intensity < self.blackout:
                        newData.append((0, 0, 0, 255))
                
                # Any other contrast value will leave colours as they are in the original,
                # when below the threshold.
                else:
                    newData.append(item)

        self.image.putdata(newData)
        self.image.save(self.saveas, "PNG")
        
        print('Exported as ', self.saveas)
        
        return True

if __name__ == "__main__":
    filename = input("Enter File Name:> ")
    saveas = input("Enter Save As Name (default: filename[:-4]):")
    threshold = input("Enter Threshold (default 600):> ")
    blackout = input("Enter Blackout Level (default 200)> ")
    contrast = input("Enter Contrast (default 3)> ")

    # Set Default Values
    if threshold == "":
        threshold = 600
    if blackout == "":
        blackout = 200
    if contrast not in ['0', '1', '2', '3']:
        contrast = 3

    
    png = draw2png(filename, threshold=600, blackout=200, contrast=int(contrast))
    
    if saveas != "":
        png.set_saveas('.\\output\\' + saveas + ".png")
    
    png.export_png()