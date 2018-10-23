let citation = null;
class Colors {
    constructor(public background, public foreground, public secondary) {

    };
}

class Bitmap {
    constructor(public data, public width, public height) {}

    draw(cit: Citation, x, y): void {
        for (let n = 0; n < this.width * this.height; n++) {
            if (this.data[n]) {
                cit.rect(x + n % this.width, y + Math.floor(n / this.width), 1, 1);
            }
        }
    };
}

class Citation {
    mainfont:string;
    altfont: string;
    multiplier:number = 2;
    width:number = 183;
    height:number = 80;

    condensed = true;
    use_alt_font = false;
    title = "";
    penalty = "";
    lines: string[] = [];

    minlines;
    lineheight;

    canvas: HTMLCanvasElement;
    context: CanvasRenderingContext2D;
    stamp: Bitmap = new Bitmap(
        [
            0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,
            0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,
            0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,
            0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,
            0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,
            0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,
            0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,
            0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,
            0,1,1,1,1,1,1,1,1,0,0,1,1,1,0,0,0,0,1,1,1,0,0,1,1,1,1,1,1,1,1,0,
            1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,
            1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,
            0,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,
            0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,
            0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,
            0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,
            0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,
            0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,
            0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,
            0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,
            0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,
            0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0
        ], 32, 32);

    color: Colors;
    private barcode_data: number[] = [1,1,1,2,2];

    constructor() {
        this.canvas = <HTMLCanvasElement>document.getElementById("main_canvas");
        this.context = this.canvas.getContext('2d');
        this.context.imageSmoothingEnabled = false;
        let form = document.getElementById("form");
        form.addEventListener("submit", (event)=>{event.preventDefault();this.refresh(); this.render(); return false});
        form.addEventListener("change", (event)=>{event.preventDefault();this.refresh(); this.render(); return false});

        this.color = new Colors("#f3d7e6", "#5a5559", "#bfa8a8");
        this.refresh();
        this.render();
    }

    refresh() {
        let fontsize = "" + (8 * this.multiplier) + "px ";
        this.mainfont = fontsize + "BMmini";
        this.altfont = fontsize + "\"Megan Serif\"";
        this.context.font = this.mainfont;

        let text = (<HTMLTextAreaElement>document.getElementsByName("text")[0]).value;
        this.penalty = (<HTMLInputElement>document.getElementsByName("penalty")[0]).value;
        this.title = (<HTMLInputElement>document.getElementsByName("title")[0]).value;
        this.condensed = (<HTMLInputElement>document.getElementsByName("condensed")[0]).checked;
        this.color.foreground = (<HTMLInputElement>document.getElementsByName("foreground")[0]).value;
        this.color.background = (<HTMLInputElement>document.getElementsByName("background")[0]).value;
        this.color.secondary = (<HTMLInputElement>document.getElementsByName("secondary")[0]).value;
        this.use_alt_font = (<HTMLInputElement>document.getElementsByName("altfont")[0]).checked;
        this.barcode_data = (<HTMLInputElement>document.getElementsByName("barcode")[0]).value
            .split(/[ ,;./|=+]/)
            .filter((a) => {return parseInt(a)})
            .map((a) => {return parseInt(a)});


        this.minlines = this.condensed ? 4 : 3;
        this.lineheight = this.condensed ? 9 : 10;


        let tmpLines = text.split("\n");
        this.lines = [];
        for (let x of tmpLines) {
            let out = this.wrapLine(x);
            this.lines.push(out[0]);
            while (out[1].length != 0) {
                out = this.wrapLine(out[1]);
                this.lines.push(out[0]);
            }
        }

        if (this.lines.length > this.minlines) {
            this.height = (80 + (this.lines.length - this.minlines) * this.lineheight);
            console.log(this.height, this.lines.length);
        } else {
            this.height = 80;
        }

        this.canvas.height = this.height * this.multiplier;
        this.canvas.width = this.width * this.multiplier;
    }

    rect(x, y, w, h) {
        return this.context.fillRect(x * this.multiplier, y * this.multiplier, w * this.multiplier, h * this.multiplier);
    }

    line(on, text) {
        this.context.fillStyle = this.color.foreground;
        let offset = 4;
        if (on != 0) {
            offset = 22 + (on - 1) * this.lineheight;
        }

        if (on == 0 && this.use_alt_font) {
            offset = 3 + 8;
            this.context.font = this.altfont;
            this.context.fillText(text.replace(" ", "    "), 11 * this.multiplier, offset * this.multiplier);
            this.context.font = this.mainfont;
        } else {
            this.context.font = this.mainfont;
            this.context.textBaseline = 'hanging';
            this.context.fillText(text, 11 * this.multiplier, offset * this.multiplier);
        }
    };

    footer(text: string, color=this.color.foreground) {
        text = text.toUpperCase();
        let y = (this.height - 15) * this.multiplier;
        let size = this.context.measureText(text);

        let x = (Math.ceil((this.width - 6 - 10 - Math.floor((size.width - 1) / this.multiplier)) / 2) + 6)* this.multiplier;
        this.context.fillText(text, x, y);
        return
    }

    dots(line: number, offset: number[], color:string=this.color.secondary) {
        this.context.fillStyle = color;
        let start = offset[0];
        let end   = this.width - 1 - offset[1];
        for (let x = 0; x < Math.floor((end - start + 1) / 2) + 1; x++) {
            this.rect(start + x*2, line, 1, 1);
        }
        return
    }

    barcode(data) {
        let end = 172;
        let width = 2;
        for (let x of data) {
            width += 1 + x
        }
        let offset = 0;
        this.context.fillStyle = this.color.foreground;
        for (let i = 0; i < data.length; i++) {
            let x = data[data.length - 1 - i];
            this.rect(end - offset - x, 3, x, 6);
            offset += 1 + x;
        }
        this.rect(end - offset - 2, 3, 2, 3);
    }

    render() {
        this.context.fillStyle = this.color.background;
        this.rect(0, 0, this.width, this.height);
        this.context.fillStyle = this.color.secondary;
        this.stamp.draw(this, 75, this.height - 4 - 32);
        this.dots(0, [0, 0]);
        this.roll();
        this.context.fillStyle = this.color.secondary;
        this.rect(this.width - 1, 0, this.width, this.height);
        this.dots(this.height - 1, [1, 0]);

        this.barcode(this.barcode_data);

        this.dots(17, [8, 10], this.color.foreground);
        this.line(0, this.title.toUpperCase());

        for (let x=0; x < this.lines.length; x++) {
            this.line(x + 1, this.lines[x]);
        }

        if (this.condensed) {
            this.dots(this.height - 22 - 1, [8, 10], this.color.foreground)
        } else {
            this.dots(this.height - 26 - 1, [8, 10], this.color.foreground)
        }
        this.footer(this.penalty)
    }

    roll() {
        for (let x=0; x < Math.floor((this.height + 3) / 9); x++) {
            this.rect(2, 3 + 9 * x, 3, 3);
            this.rect(this.width - 7, 3 + 9 * x, 3, 3);
        }
    }

    wrapLine(text: string): string[] {
        let max_w = (this.width - 11 - 12) * this.multiplier;
        let size = this.context.measureText(text);
        if (size.width <= max_w) {
            return [text, ""];
        }
        let chars = 1;
        size = this.context.measureText(text.substring(0, chars));
        while (size.width < max_w) {
            size = this.context.measureText(text.substring(0, chars));
            chars += 1;
        }
        return [text.substring(0, chars - 1), text.substring(chars - 1)]
    }

    static init() {
        citation = new Citation();
    }
}


document.addEventListener("DOMContentLoaded", Citation.init, false);
