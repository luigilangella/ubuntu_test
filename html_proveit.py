def html_email(ref):
    html = f"""\
<!DOCTYPE html>
    <html>  
        <body>
            <div class="WordSection1">
                <p style="text-align: center;" align="center">&nbsp;</p>
                <p style="text-align: center;" align="center"><img id="Picture_x0020_1" style="width: 299px; height: 92px;" src="https://i.ibb.co/hVVSV4B/Prove-IT.jpg" alt="proveit-logo" width="199" height="61" /></p>
                <p style="text-align: center;" align="center"><img id="Picture_x0020_2" style="width: 185px; height: 70px;" src="https://i.ibb.co/XktsTJR/Kier-png.jpg" alt="kier-logo" width="123" height="47" /></p>
                <p style="text-align: center;" align="center"><strong><span style="font-size: 12.0pt; font-family: 'Arial',sans-serif; color: black;">{ref} : Prove-IT STATS Pack</span></strong></p>
                <p style="text-align: center;" align="center"><strong><span style="font-size: 12.0pt; font-family: 'Arial',sans-serif; color: black;">&nbsp;</span></strong></p>
                <p style="text-align: center;" align="center">Whilst every effort has been taken to ensure the accuracy of the data in the attached STATS Pack the information enclosed should not be used for any purpose other than as a general guide to the location of existing services.</p>
                <p style="text-align: center;" align="center">For help and support please email GIS@kier.co.uk</p>
                <p class="MsoNormal">&nbsp;</p>
            </div>
        </body>
    </html>"""
    return html

def html_email_download(ref, hyperlink):
    html = f"""\
<!DOCTYPE html>
    <html>  
        <body>
            <div>
               <p align="center">&nbsp;</p>
                <p style="text-align: center;" align="center"><img id="Picture_x0020_1" style="width: 299px; height: 92px;" src="https://i.ibb.co/hVVSV4B/Prove-IT.jpg" alt="proveit-logo" width="199" height="61" /></p>
                <p style="text-align: center;" align="center"><img id="Picture_x0020_2" style="width: 185px; height: 70px;" src="https://i.ibb.co/XktsTJR/Kier-png.jpg" alt="kier-logo" width="123" height="47" /></p>
                <p style="text-align: center;" align="center"><strong><span style="font-size: 12.0pt; font-family: 'Arial',sans-serif; color: black;">{ref} : Prove-IT STATS Pack</span></strong></p>
                <div style="text-align: center;">
                    <div>
                        <table style="border-collapse: separate; line-height: 100%;" role="presentation" border="0" cellspacing="0" cellpadding="0" align="center">
                            <tbody>
                                <tr>
                                    <td style="border: none; border-radius: 6px; cursor: auto; padding: 11px 20px; background: #51698f;" role="presentation" align="center" valign="middle" bgcolor="#19cca3"><a style="background: #51698f; color: #ffffff; font-family: Arial, Helvetica, sans-serif; font-size: 18px; font-weight: 600; line-height: 120%; margin: 0; text-decoration: none; text-transform: none;" href="{hyperlink}" target="_blank" rel="noopener"> Download&nbsp;</a></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <p style="text-align: center;" align="center">Whilst every effort has been taken to ensure the accuracy of the data in the attached STATS Pack the information enclosed should not be used for any purpose other than as a general guide to the location of existing services.</p>
                <p style="text-align: center;" align="center">For help and support please email GIS@kier.co.uk</p>
                <p class="MsoNormal">&nbsp;</p>
            </div>
        </body>
    </html>"""
    return html
