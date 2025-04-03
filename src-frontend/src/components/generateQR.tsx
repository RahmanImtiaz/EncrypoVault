import QRCode from "react-qr-code";
import { FC } from "react";


interface QRCodeProps {
    value: string;
    size?: number;
    level?: "L" | "M" | "Q" | "H";
    bigColor?: string;
    fgColor?: string;
    className?: string;
}


export const QRCodeComponent: FC<QRCodeProps> = ({
    value,
    size = 128,
    level = 'Q',
    bigColor = '#ffffff',
    fgColor = '#000000',
    className = ''

}) => {
    if (!value) {
        return null; 
    }

    return (
        <div className={`qr-code-container ${className}`}>
            <QRCode
                value={value}
                size={size}
                level={level}
                bgColor={bigColor}
                fgColor={fgColor}
                style={{ width: size, height: size }}
            />
        </div>
    );

}