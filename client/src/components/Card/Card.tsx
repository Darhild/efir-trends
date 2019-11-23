import React, { Component } from 'react';
import classnames from 'classnames';
import './Card.scss';
import { changeImageSize } from '../../utils/images';

export interface Props {
    id: string;
    title?: React.ReactNode;
    subtitle?: React.ReactNode;
    details?: React.ReactNode;
    rightContent?: React.ReactNode;
    className?: string;
    img?: string;
    imgView?: string;
    size?: string;
    poster?: string;
    bgColor?: string;
}

export default class Card extends Component<Props> {
    public renderContent() {
        const {
            title,
            subtitle,
            rightContent,
        } = this.props;

        const titles = (
            <>
                {title && <div className="Card-Title" >{title}</div>}
                {subtitle && <div className="Card-Subtitle">{subtitle}</div>}
            </>
        );

        if (rightContent) {
            return (
                <div className="Card-Content Card-Content_view_grid">
                    <div className="Card-Left">{titles}</div>
                    <div className="Card-Right">{rightContent}</div>
                </div>
            );
        }

        return <div className="Card-Content">{titles}</div>;
    }

    public render() {
        const {
            className,
            size = 'medium',
            id,
            img,
            imgView,
            details,
            poster,
            bgColor,
        } = this.props;

        const cardCn = classnames(
            'Card',
            `Card_size_${size}`,
            bgColor && `Card_bgColor_${bgColor}`,
            className,
        );

        const thumbCn = classnames(
            'Card-Thumb',
            imgView && `Card-Thumb_view_${imgView}`,
        );

        return (
            <a
                className={cardCn}
                href={`https://yandex.ru/efir?from=efir&stream_id=${id}`}
                target="_blank"
                rel="noopener noreferrer"
            >
                <div
                    className={thumbCn}
                    style={{ backgroundImage: img ? `url(${changeImageSize(img)})` : '' }}
                >
                    {
                        poster && <img src={changeImageSize(poster, '200x150')} className="Card-Poster" alt="" />
                    }
                    {
                        details && <div className="Card-Details">{details}</div>
                    }
                </div>
                {this.renderContent()}
            </a>
        );
    }
}
