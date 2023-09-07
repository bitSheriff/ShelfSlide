# ShelfSlide

<img src="./doc/logo.jpeg"
     alt="Logo"
     width="300"
/>

> :warning: **This project is still in development and not ready for production use.**

ShelfSlide is an open-source project that turns your Raspberry Pi and E-Ink display into a stylish digital bookshelf. It allows you to showcase the book covers of your favorite eBooks that you've read or want to show off. ShelfSlide is designed to be simple to set up and highly customizable, allowing you to personalize your digital bookshelf with ease.

## Idea

I am hugh bookworm and love to read on my eReaders. The one thing I miss is the kind of private library which builds up year after year. The book covers are a great way to remember the books you've read and to show them to others. So I thought why not build a digital bookshelf which can be used to display the book covers of my eBooks.

### Isn't there such a thing?

Well, yes and no.
There is a very awesome project called [Openframe](https://openframe.io/), which can be used to show digital art on a screen. Unfortunately the do not support e-Ink devices (yet).

## Features

- Display book covers of your eBooks on an E-Ink display.
- Automatically download book covers from provided URLs or use simple JPG files.
- Customize the display order and layout of your bookshelf.
- Easily add, remove, or update books using a JSON configuration file.
- Minimal power consumption thanks to E-Ink technology.
- Perfect for creating a digital library or showcasing your literary collection.

> :warning: **Copyright Infringement Risk** Important Notice for Users :warning:
> 
> Using the online functions provided in this software that allow you to download content from external links may pose a significant risk of copyright infringement. It is essential to be aware of and respect copyright laws and regulations before utilizing this feature.
> <underline> Please check the right before using this feature.</underline>

## Getting Started

Follow these simple steps to set up your ShelfSlide digital bookshelf:

### Prerequisites

- Raspberry Pi (Model 3 or later recommended)
- E-Ink display compatible with Raspberry Pi (e.g., Waveshare)
- Python 3.x installed on your Raspberry Pi

### Installation

1. Install the required packages on the Raspberry Pi:

   ```shell
   sudo apt-get install python3-pip
   sudo apt-get install libopenjp2-7
   ```

2. Clone the ShelfSlide repository to your Raspberry Pi:

   ```shell
   git clone https://github.com/bitSheriff/ShelfSlide.git
   ```

3. Navigate to the project directory:

   ```shell
   cd ShelfSlide
   ```

4. Create virtual environment and active it:

   ```shell
   python3 -m venv venv
   sourve venv/bin/activate
   ```

5. Install the required Python packages:

   ```shell
   pip install -r requirements.txt
   ```

### Configuration

The configuration is done with the file `config.yaml`.

`books.dir`
Directory where the `books.json` file is located.

`books.git`
If set to `true` the `books.json` file and `media/`will be pulled from the git repository.

`books.clean`
If set to `true` the downloaded covers will get removed every time at startup.

`slideshow.interval`
Interval in seconds between the covers.

`slideshow.mode`
Mode of the slideshow. Can be `random`, `asc` or `desc` which stands for random, ascending or descending order (decided on the date the book was read).

`display.com`
Communication interface of the display. Can be `spi` or `hdmi`. Many EPD (electronic paper display -> e-Ink) displays are connected via SPI, but some are connected via HDMI.

`display.height`
Height of the display in pixels.

`display.width`
Width of the display in pixels.

### Usage

#### Run ShelfSlide:

To start the application just execute the python file in the root directory of the project.

```shell
python shelfslide.py
```

#### Adding books

## Contributing

We welcome contributions from the community to improve ShelfSlide. If you'd like to contribute, please follow these guidelines:

1. Fork the repository and create a new branch for your feature or bug fix.
2. Make your changes and test them thoroughly.
3. Ensure your code follows the project's coding style and conventions.
4. Submit a pull request with a clear description of your changes and the problem you're solving.

## License

ShelfSlide is open-source software licensed under the [MIT License](LICENSE).

## Acknowledgments

ShelfSlide was inspired by the love of books and the desire to create a unique way to display and share your reading list with others. We'd like to thank the open-source community for their support and contributions.

---

Enjoy showcasing your literary adventures with ShelfSlide! If you have any questions, suggestions, or issues to report, please [open an issue](https://github.com/bitSheriff/ShelfSlide/issues) on GitHub. Happy reading!
