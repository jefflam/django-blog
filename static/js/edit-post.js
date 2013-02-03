// Display top menu bar on mouse over, hide it on mouse leave
// For less visual distraction
$('.navbar').hover(
    function() {
        $(this).css('opacity', '1');
    },
    function() {
        $(this).css('opacity', '0');
    }
);

// Using jquery.autosize library, allow textareas to expand
// as more text is typed into textarea box
$('textarea').autosize();