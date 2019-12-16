$(function() {
  // $('.image .disabled_checkbox').click(function() {
  //   return false;
  // });

  $('.thumbnail').each(function(index, element){
      if ($(element).next().prop('checked')){
          $(element).addClass('checked');
      }
  });

  $('.possession-checkbox').click(function() {
      if ($(this).attr('data-checked') == 'false') {
          // console.log('checkbox true');
          // console.log($(this).attr('data-checked'));
          $(this).prev().addClass('checked');
          $(this).attr('data-checked', 'true');
          // $(this).text('✓');
      } else {
          // console.log('checkbox false');
          // console.log($(this).attr('data-checked'));
          $(this).prev().removeClass('checked');
          $(this).attr('data-checked', 'false');
          // $(this).text('');
      }

      $.ajax({
        url: '/cards/update_possession',
        type: 'POST',
        data: {
          id: $(this).attr('id'),
          pos: $(this).attr('data-checked')
        }
      })
  });

  $('.image').click(function() {
    $('.image').each(function(index, element){
        $(element).removeClass('checked');
    });
    $(this).addClass('checked');

    checkbox = $(this).find('.possession-checkbox');
    kind = checkbox.attr('data-kind');
    id = checkbox.attr('id');
    image_filename = 'card-' + ('000'+id).substr(-3) + '.jpg'
    card_src = `/assets/card/${kind}/${image_filename}`
    $('#card').attr('src', card_src);

    if (kind.slice(0, 1) == 'p') {
        $('.idea').addClass('hidden');
    } else if (kind.slice(0, 1) == 's') {
        $('.idea').removeClass('hidden');
    }
  });
});