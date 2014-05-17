//JS to convert between IPA and SAMPA
//GPL licenced by Paolo Mairano
//Modified by me (KJ) to strip out the DOM related stuff so it can run under node


// definisci equiv ed equiv2
var equiv = ['ɛ', 'E', 'ɑ', 'A', 'ɔ', 'O', 'ø', '2', 'œ', '9', 'ɶ', '&', 'ɒ', 'Q', 'ʌ', 'V', 'ɤ', '7', 'ɯ', 'M', 'ɪ', 'I', 'ʏ', 'Y', 'æ', '{', 'ʊ', 'U', 'ɨ', '1', 'ʉ', '}', 'ɘ', '@\\', 'ɵ', '8', 'ə', '@', 'ɜ', '3', 'ɞ', '3\\', 'ɐ', '6', '̪', '_d', '̠', '_-', 'ʈ', 't`', 'ɖ', 'd`', 'ɟ', 'j\\', 'g', 'g', 'ɢ', 'G\\', 'ʔ', '?', '̥', '_0', 'ɱ', 'F', 'ɳ', 'n`', 'ɲ', 'J', 'ŋ', 'N', 'ɴ', 'N\\', 'ʙ', 'B\\', 'ʀ', 'R', 'ɾ', '4', 'ɽ', 'r`', 'ɸ', 'p\\', 'β', 'B', 'θ', 'T', 'ð', 'D', 'ʃ', 'S', 'ʒ', 'Z', 'ʂ', 's`', 'ʐ', 's`', 'ç', 'C', 'ʝ', 'j\\', 'ɣ', 'G', 'χ', 'X', 'ʁ', 'R', 'ħ', 'X\\', 'ʕ', '?\\', 'ɦ', 'h\\', 'ɬ', 'K', 'ɮ', 'K\\', '̞', '_o', 'ɹ', 'r\\', 'ɻ', 'r\\`', 'ɰ', 'M\\', 'ɭ', 'l`', 'λ', 'L', 'ʟ', 'L\\', 'ʘ', 'O\\', 'ǀ', '|\\', 'ǃ', '!\\', 'ǂ', '=\\', 'ɓ', 'b_<', 'ɗ', 'd_<', 'ʄ', 'j\_<', 'ɠ', 'g_<', 'ʛ', 'G\_<', 'ʼ', '_>', 'ʍ', 'W', 'ɥ', 'H', 'ʢ', '<\\', 'ɕ', 's\\', 'ɺ', 'l\\', 'ʜ', 'H\\', 'ʡ', '>\\', 'ʑ', 'z\\', 'ɧ', 'x\\', 'ː', ':', 'ˑ', ':\\', 'ˑ', '.', '̩', '_=', '̩', '=', '̃', '~', '̃', '_~', 'ˈ', '"', 'ˌ', '%', ' ̈', '_"', '̟', '_+', '̠', '_-', 'ˇ', '_/', '̥', '_0', 'ˤ', '_?\\', 'ˆ', '_\\', '̯', '_^', '̚', '_}', '̘', '_A', '̺', '_a', '᷅', '_B_L', '̏', '_B', '̜', '_c', '̪', '_d', '̴', '_e', '̂', '_F', 'ˠ', '_G', '᷄', '_H_T', '́', '_H', 'ʲ', '_j', '̰', '_k', '̀', '_L', 'ˡ', '_l', '̄', '_M', '̻', '_m', '̼', '_N', 'ʰ', '_h', 'ⁿ', '_n', '̹', '_O', '̞', '_o', '̙', '_q', '᷈', '_R_F', '̌', '_R', '̝', '_r', '̋', '_T', '̤', '_t', '̬', '_v', 'ʷ', '_w', '̆', '_X', '̽', '_x'];
var equiv2 = new Array();
for (var i=0; i<equiv.length; i++) {
	equiv2[i] = equiv[i].replace(/\\/g, '\\\\'); // evita potenziali errori creati dai simboli SAMPA
	equiv2[i] = equiv2[i].replace(/\?/g, '\\?'); // evita potenziali errori creati dai simboli SAMPA
	equiv2[i] = equiv2[i].replace(/\|/g, '\\|'); // evita potenziali errori creati dai simboli SAMPA
	equiv2[i] = equiv2[i].replace(/\+/g, '\\+'); // evita potenziali errori creati dai simboli SAMPA
	equiv2[i] = equiv2[i].replace(/\-/g, '\\-'); // evita potenziali errori creati dai simboli SAMPA
	equiv2[i] = equiv2[i].replace(/\{/g, '\\{'); // evita potenziali errori creati dai simboli SAMPA
	equiv2[i] = equiv2[i].replace(/\}/g, '\\}'); // evita potenziali errori creati dai simboli SAMPA
	equiv2[i] = equiv2[i].replace(/\=/g, '\\='); // evita potenziali errori creati dai simboli SAMPA
	equiv2[i] = equiv2[i].replace(/\</g, '\\<'); // evita potenziali errori creati dai simboli SAMPA
	equiv2[i] = equiv2[i].replace(/\>/g, '\\>'); // evita potenziali errori creati dai simboli SAMPA
	equiv2[i] = equiv2[i].replace(/\./g, '\\.'); // evita potenziali errori creati dai simboli SAMPA
	equiv2[i] = equiv2[i].replace(/\,/g, '\\,'); // evita potenziali errori creati dai simboli SAMPA
	equiv2[i] = equiv2[i].replace(/\:/g, '\\:'); // evita potenziali errori creati dai simboli SAMPA
	equiv2[i] = equiv2[i].replace(/\;/g, '\\;'); // evita potenziali errori creati dai simboli SAMPA
	equiv2[i] = equiv2[i].replace(/\^/g, '\\^'); // evita potenziali errori creati dai simboli SAMPA
}

function ipatosampa (testo) {
		
		var reg = '';
		
		// cerca se c'é un equivalente
		for (var i=0; i<equiv.length; i=i+2) {
			reg = new RegExp (equiv[i], 'g');
			testo = testo.replace(reg, equiv[i+1]);
		}
		
		return (testo);
}

function sampatoipa (testo) {
		
		var reg = '';
		
		// evita che si creino errori di slash
		testo = testo.replace(/\\/g, '');
		
		// cerca se c'é un equivalente
		for (var i=1; i<=equiv2.length; i=i+2) {
			reg = new RegExp (equiv2[i], 'g');
			testo = testo.replace(reg, equiv2[i-1]);
		}
		
		return (testo);
}


//Look at command line arguments (for node.js)
//Form: ipa2xsampa xxx or xsampa2ipa xxxx

var direction = process.argv[2];

var phon = "";
process.stdin.setEncoding('utf8');
process.stdin.on('readable', function(){
        var chunk = process.stdin.read();
        if (chunk != null)
            phon += chunk;
});

process.stdin.on('end', function(){
    //process.stdout.write('Doing ' + direction + '\n');
    if (direction == 'ipa2xsampa') {
        process.stdout.write(ipatosampa(phon));
    }
    else if (direction == 'xsampa2ipa') {
        process.stdout.write(sampatoipa(phon));
    }
});


