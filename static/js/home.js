// ---------------------------------------------------------------
    // PART 1: Banner slider
    // ---------------------------------------------------------------
    var slides = document.querySelectorAll(".banner__slide");
    var dots = document.querySelectorAll(".banner__dot");
    var currentSlide = 0;

    // Show the slide with the given number (0 = first slide)
    function showSlide(number) {
        // Hide the current slide and dot
        slides[currentSlide].classList.remove("active");
        dots[currentSlide].classList.remove("active");

        // If we go past the last slide, start from the first one again
        if (number >= slides.length) {
            number = 0;
        }
        // If we go before the first slide, jump to the last one
        if (number < 0) {
            number = slides.length - 1;
        }

        // Show the new slide and dot
        currentSlide = number;
        slides[currentSlide].classList.add("active");
        dots[currentSlide].classList.add("active");
    }

    function nextSlide() {
        showSlide(currentSlide + 1);
    }

    function prevSlide() {
        showSlide(currentSlide - 1);
    }

    // Change the slide automatically every 5 seconds (only if there is more than one)
    if (slides.length > 1) {
        setInterval(nextSlide, 5000);
    }


    // ---------------------------------------------------------------
    // PART 2: Countdown timer (counts down to midnight)
    // ---------------------------------------------------------------

    // Add a leading zero, for example 5 becomes "05"
    function addZero(number) {
        if (number < 10) {
            return "0" + number;
        }
        return String(number);
    }

    function updateCountdown() {
        var now = new Date();
        var midnight = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1);

        var secondsLeft = Math.floor((midnight - now) / 1000);
        var hours = Math.floor(secondsLeft / 3600);
        var minutes = Math.floor((secondsLeft % 3600) / 60);
        var seconds = secondsLeft % 60;

        document.getElementById("deal-hours").textContent = addZero(hours);
        document.getElementById("deal-mins").textContent = addZero(minutes);
        document.getElementById("deal-secs").textContent = addZero(seconds);
    }

    updateCountdown();                    // run once immediately
    setInterval(updateCountdown, 1000);   // then run every 1 second


    // ---------------------------------------------------------------
    // PART 3: Fade-in animation when an element scrolls into view
    // ---------------------------------------------------------------
    var revealItems = document.querySelectorAll(".reveal");

    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            // If the element is visible on screen, add the "show" class
            if (entry.isIntersecting) {
                entry.target.classList.add("show");
            }
        });
    }, { threshold: 0.15 });

    revealItems.forEach(function (item) {
        observer.observe(item);
    });
