$('.alert').fadeTo(5000,500).slideUp(500, () => $('.alert').slideUp(500))

$('#instrument_select').change(function(){
    const opt = $(this).children("option:selected").val()
    if (opt == "hvlt"){
        $('#total_score').text('Total Score of trials 1-3')
    }
    else if (opt != "hvlt"){
        $('#total_score').text('Total Score of trials 1-5')
    }
})
// $('#instrument_select').change(function(){
//     localStorage.setItem('instrument', $('#instrument_select option:selected').text())
//     $('#instrument_select option:selected').text(localStorage.getItem('instrument'))
// })
// $('#item_select').change(function(){
//     localStorage.setItem('item', $('#item_select option:selected').text())
//     $('#item_select option:selected').text(localStorage.getItem('item'))
// })
// $('#formGroupExampleInput').change(function () {
//   localStorage.setItem('score', $('#formGroupExampleInput').val())
//   $('#formGroupExampleInput').val(localStorage.getItem('score'))
// })
