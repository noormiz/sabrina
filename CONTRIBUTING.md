# Contributing to SABRINA

Thank you for your interest in contributing to SABRINA! This document provides guidelines and instructions for contributing to this open-source educational project.

## 🤝 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/sabrina.git
   cd sabrina
   ```
3. **Create a new branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes** and test them
5. **Commit your changes** with clear messages:
   ```bash
   git commit -m "Add: Description of your change"
   ```
6. **Push to your fork** and create a Pull Request

## 📋 Contribution Guidelines

### Reporting Bugs

- Use the GitHub Issues tracker
- Include a clear title and description
- Provide steps to reproduce the bug
- Include screenshots if applicable
- Specify your environment (OS, browser, Python version)

### Suggesting Features

- Open an issue with the "enhancement" label
- Describe the feature and its educational value
- Explain how it fits with SABRINA's goals
- Consider implementation complexity

### Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Ensure all tests pass**
4. **Follow code style** (see below)
5. **Write clear commit messages**
6. **Reference related issues** in your PR

## 💻 Development Setup

### Prerequisites
- Python 3.8+
- pip
- Git

### Setup Steps

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables:**
   ```bash
   export GEMINI_API_KEY="your-key-here"  # Optional
   export SECRET_KEY="your-secret-key"    # Optional
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Run tests:**
   ```bash
   python test_mission_core.py
   python test_ai_feedback.py
   ```

## 📝 Code Style

### Python
- Follow PEP 8 style guide
- Use descriptive variable names
- Add docstrings to functions and classes
- Keep functions focused and small
- Comment complex logic

### JavaScript
- Use ES6+ syntax
- Use meaningful variable names
- Add comments for complex logic
- Follow consistent indentation (2 spaces)

### HTML/CSS
- Use semantic HTML
- Follow consistent indentation
- Use meaningful class names
- Keep CSS organized and commented

## 🎯 Areas for Contribution

### High Priority

1. **New Exoplanets**
   - Add real exoplanets with accurate parameters
   - Include atmospheric data if available
   - Add appropriate emoji icons
   - Update `mission_core.py` EXOPLANETS dictionary

2. **Interactive Activities**
   - Create new science activities
   - Implement interactive visualizations
   - Add educational content
   - Examples: Gravitational lensing, radio astronomy, stellar classification

3. **UI/UX Improvements**
   - Improve animations and transitions
   - Enhance responsive design
   - Better mobile experience
   - Accessibility improvements (screen readers, keyboard navigation)

4. **Educational Content**
   - Add more "Learn More" sections
   - Create tutorial videos or guides
   - Improve tooltips and help text
   - Add quizzes or assessments

### Medium Priority

5. **Testing**
   - Add more unit tests
   - Create integration tests
   - Add end-to-end tests
   - Improve test coverage

6. **Performance**
   - Optimize loading times
   - Implement caching
   - Reduce bundle size
   - Optimize API calls

7. **Documentation**
   - API documentation
   - Developer guides
   - User manuals
   - Video tutorials

8. **Features**
   - Teacher dashboard
   - Progress tracking
   - Multiplayer missions
   - 3D visualizations

### Low Priority

9. **Internationalization**
   - Translate to other languages
   - Add language switcher
   - Localize content

10. **Mobile App**
    - React Native version
    - Native mobile features
    - Offline support

## 🔬 Adding New Exoplanets

To add a new exoplanet:

1. Research the exoplanet's real parameters:
   - Distance from Earth
   - Mass and radius
   - Orbital period
   - Surface temperature
   - Atmospheric composition (if known)

2. Add to `mission_core.py`:
   ```python
   EXOPLANETS = {
       "YourExoplanetName": {
           "name": "Display Name",
           "type": "Planet Type",
           "distance": "X Light Years",
           "icon_emoji": "🌍",
           "simDistanceKm": 15000000,  # Scaled for gameplay
           "gravityFactor": 1.0,
           "atmosphereDrag": 0.3,
           "atmosphere_elements": ["Element1", "Element2"],
           # ... other parameters
       }
   }
   ```

3. Test the exoplanet in the mission flow
4. Update documentation

## 🎮 Adding New Activities

To add a new interactive activity:

1. Create a new template in `templates/`
2. Add a route in `app.py`
3. Implement the activity logic
4. Add educational content
5. Test thoroughly
6. Update navigation and documentation

## 🐛 Testing

- Run existing tests before submitting PR
- Add tests for new features
- Test on multiple browsers
- Test on different screen sizes
- Test with and without API key

## 📚 Documentation

- Update README.md for major changes
- Add docstrings to new functions
- Update CONTRIBUTING.md if process changes
- Add comments for complex code

## 🎨 Design Guidelines

- Keep the educational focus
- Maintain age-appropriate content (11-14 years)
- Use clear, readable fonts
- Ensure good color contrast
- Make interactive elements obvious
- Provide visual feedback

## ❓ Questions?

- Open an issue with the "question" label
- Check existing issues and discussions
- Review the code and documentation

## 🙏 Thank You!

Your contributions help make SABRINA better for students and educators worldwide. Every contribution, no matter how small, is appreciated!

---

**Happy coding! 🚀**

