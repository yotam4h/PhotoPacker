# PhotoPacker

A professional tool for creating photo collages with exact physical dimensions, perfect for printing.

## Features

- Create collages with precise physical dimensions (cm)
- Organize photos by target print sizes
- Maintain exact aspect ratios
- Optimize layouts for standard paper sizes (A4, A3, etc.)
- Professional print quality (300 DPI default)

## Installation

### From PyPI (recommended)

```bash
pip install photopacker
```

### From source

```bash
git clone https://github.com/yotam4h/PhotoPacker.git
cd PhotoPacker
pip install .
```

## Usage

### Basic usage

```bash
photopacker -i input_directory -o output_directory
```

### Command-line options

```
usage: photopacker [-h] -i INPUT -o OUTPUT [--page-size {a4,a3,letter,legal}]
                  [--dpi DPI] [--margin MARGIN] [-v]

PhotoPacker - Create photo collages with exact physical dimensions

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input directory containing size-named folders
  -o OUTPUT, --output OUTPUT
                        Output directory for collages
  --page-size {a4,a3,letter,legal}
                        Page size (default: a4)
  --dpi DPI             Output resolution in DPI (default: 300)
  --margin MARGIN       Margin between images in millimeters (default: 2mm)
  -v, --verbose         Enable verbose output
```

### Input directory structure

Your input directory should contain folders named by the target print size in centimeters:

```
input/
  10_10/     (for 10×10cm images)
  10_15/     (for 10×15cm images)
  13_18/     (for 13×18cm images)
  20_25/     (for 20×25cm images)
  ...
```

Each folder should contain the images you want printed at that size.

### Examples

Create A4 collages with default settings:
```bash
photopacker -i input -o output
```

Create A3 collages:
```bash
photopacker -i input -o output --page-size a3
```

Use 5mm margins between photos:
```bash
photopacker -i input -o output --margin 5
```

Lower resolution for faster processing:
```bash
photopacker -i input -o output --dpi 150
```

## API Usage

You can also use PhotoPacker as a library in your Python code:

```python
from photopacker.core import PhotoPacker

# Create a PhotoPacker instance
packer = PhotoPacker(
    input_dir="input",
    output_dir="output",
    page_size="a4",  # 'a4', 'a3', 'letter', 'legal'
    dpi=300,
    margin_mm=2
)

# Process images
exit_code = packer.process()
```

## Credits

### Example Photos

The example photos included in this repository are provided by the following photographers on [Unsplash](https://unsplash.com/):

- [Jose Matute](https://unsplash.com/@jematutef)
- [Ahmed Yameen](https://unsplash.com/@yammiien)
- [Dim Gunger](https://unsplash.com/@gundim)
- [Ali Nejatian](https://unsplash.com/@ali_nejatian)
- [Sour Moha](https://unsplash.com/@sour_moha)
- [Li Lin](https://unsplash.com/@incrprl)
- [Stepan Kalinin](https://unsplash.com/@northwoodn)

Photos from Unsplash are licensed under the [Unsplash License](https://unsplash.com/license), which grants permission for commercial and non-commercial use without attribution (though attribution is appreciated).

## License

MIT License