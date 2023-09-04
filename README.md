# ShelfSlide

<img src="./doc/logo.jpeg"
     alt="Logo"
     width="300"
/>

ShelfSlide is an open-source project that turns your Raspberry Pi and E-Ink display into a stylish digital bookshelf. It allows you to showcase the book covers of your favorite eBooks that you've read or want to show off. ShelfSlide is designed to be simple to set up and highly customizable, allowing you to personalize your digital bookshelf with ease.

## Idea

### Isn't there such a thing?

Well, yes and no.
There is a very awesome project called [Openframe](https://openframe.io/)

## Features

- Display book covers of your eBooks on an E-Ink display.
- Automatically download book covers from provided URLs or use simple JPG files.
- Customize the display order and layout of your bookshelf.
- Easily add, remove, or update books using a JSON configuration file.
- Minimal power consumption thanks to E-Ink technology.
- Perfect for creating a digital library or showcasing your literary collection.

## Getting Started

Follow these simple steps to set up your ShelfSlide digital bookshelf:

### Prerequisites

- Raspberry Pi (Model 3 or later recommended)
- E-Ink display compatible with Raspberry Pi (e.g., Waveshare)
- Python 3.x installed on your Raspberry Pi

### Installation

1. Clone the ShelfSlide repository to your Raspberry Pi:

   ```shell
   git clone https://github.com/bitSheriff/ShelfSlide.git
   ```

2. Navigate to the project directory:

   ```shell
   cd ShelfSlide
   ```

3. Install the required Python packages:

   ```shell
   pip install -r requirements.txt
   ```

### Configuration

The configuration is done with the file `config.yaml`.

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
