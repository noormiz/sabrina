# 🚀 SABRINA: Space Mission Simulator for Future Astronauts

> **An open-source, educational web application that transforms complex aerospace and astrobiology concepts into an accessible, engaging learning experience for middle school students.**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](CONTRIBUTING.md)

## 🌟 Overview

SABRINA is a web-based, data-driven simulation designed to teach middle school students (Ages 11-14) about:
- **Orbital Mechanics** - Launch, cruise, and landing physics
- **Exoplanet Science** - Real NASA data and discovery techniques
- **Atmospheric Spectroscopy** - Analyzing planetary atmospheres
- **Transit Photometry** - Detecting exoplanets through light curves
- **Mission Planning** - Fuel management and trajectory optimization

## ✨ Features

- 🎮 **Interactive Mission Simulation** - Complete mission cycle from launch to return
- 🪐 **Real Exoplanet Data** - Uses actual NASA exoplanet parameters (Proxima Centauri b, TRAPPIST-1e, Kepler-452b)
- 🤖 **AI-Powered Tutor** - Google Gemini AI provides personalized learning support
- 📊 **Interactive Activities** - Hands-on spectroscopy and photometry mini-games
- 🏆 **Achievement System** - Badges and rewards for successful missions
- 📱 **Social Sharing** - Share mission achievements with friends
- 🎯 **Educational Focus** - Teaches real aerospace concepts through gameplay

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key (optional, for AI tutor feature)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/noormiz/sabrina.git
   cd sabrina
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables (optional):**
   ```bash
   # Windows PowerShell
   $env:GEMINI_API_KEY="your-api-key-here"
   $env:SECRET_KEY="your-secret-key-here"

   # Linux/Mac
   export GEMINI_API_KEY="your-api-key-here"
   export SECRET_KEY="your-secret-key-here"
   ```

4. **Run the application:**
   ```bash
   # Windows PowerShell
   python app.py
   # Or use the provided script
   .\start_server.ps1

   # Linux/Mac
   python app.py
   ```

5. **Open your browser:**
   Navigate to `http://localhost:5000`

## 📁 Project Structure

```
sabrina/
├── app.py                 # Flask application and routes
├── mission_core.py        # Core mission logic and physics
├── ai_feedback.py         # AI tutor integration
├── requirements.txt       # Python dependencies
├── start_server.ps1       # Windows server startup script
├── templates/             # HTML templates
│   ├── welcome.html       # Welcome screen
│   ├── index.html         # Main mission interface
│   ├── spectroscopy.html  # Spectroscopy activity
│   └── transit_photometry.html  # Photometry activity
├── test_mission_core.py   # Unit tests
└── test_ai_feedback.py    # AI feedback tests
```

## 🎓 Educational Goals

SABRINA teaches students:
- **Physics Concepts**: Thrust-to-weight ratio, escape velocity, orbital mechanics
- **Space Mission Planning**: Fuel management, trajectory optimization
- **Exoplanet Science**: Real NASA discovery techniques and data
- **Scientific Method**: Hypothesis testing, data collection, analysis
- **Problem Solving**: Critical thinking and decision-making

## 🔧 Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **AI Integration**: Google Gemini API
- **Visualization**: SVG animations, Canvas API
- **Data**: Real NASA exoplanet parameters

## 📊 Project Status

**Current Status: Project Complete (v1.0)**

SABRINA v1.0 is complete and fully functional with all core features implemented:
- ✅ Complete mission simulation (launch, cruise, landing, return)
- ✅ Interactive science activities (spectroscopy, photometry)
- ✅ AI-powered tutoring system
- ✅ Real exoplanet data integration
- ✅ Achievement and sharing system

**This version is stable and ready for use in educational settings.**

While the core project is complete, we welcome contributions from the open-source community to enhance and extend SABRINA. See the [Roadmap](#-roadmap--future-work) section for ideas on how you can contribute.

## 🤝 Contributing

We welcome contributions! SABRINA is an open-source project, and we'd love your help making it better.

**Ways to contribute:**
- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🎨 Enhance UI/UX
- 🔬 Add new exoplanets or activities
- 🧪 Write tests
- 🌍 Translate to other languages

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 🗺️ Roadmap & Future Work

### Planned Features
- [ ] 3D visualization of trajectories
- [ ] Multiplayer missions
- [ ] Additional exoplanets (Kepler-1649c, LHS 1140 b, etc.)
- [ ] More interactive activities (gravitational lensing, radio astronomy)
- [ ] Teacher dashboard for classroom use
- [ ] Progress tracking and analytics
- [ ] Mobile app version
- [ ] Multi-language support

### Areas for Contribution
- **New Exoplanets**: Add more real exoplanets with accurate parameters
- **Activities**: Create new interactive science activities
- **UI/UX Improvements**: Better animations, responsive design
- **Educational Content**: More learning resources, tutorials
- **Accessibility**: Screen reader support, keyboard navigation
- **Performance**: Optimization, caching, loading times
- **Testing**: More unit tests, integration tests
- **Documentation**: API docs, developer guides

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution ideas.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **NASA Exoplanet Archive** - For real exoplanet data
- **Google Gemini API** - For AI tutoring capabilities
- **Educational Community** - For inspiration and feedback

## 📧 Contact

- **GitHub Issues**: [Report bugs or request features](https://github.com/noormiz/sabrina/issues)
- **Discussions**: [Join the conversation](https://github.com/noormiz/sabrina/discussions)

## 🌟 Show Your Support

If you find SABRINA useful, please consider:
- ⭐ Starring this repository
- 🐛 Reporting bugs
- 💡 Suggesting improvements
- 🔄 Sharing with educators and students

---

**Made with ❤️ for future astronauts and space enthusiasts**

*"The universe is under no obligation to make sense to you."* - Neil deGrasse Tyson
