@bot.tree.command(name="check")
async def check(interaction: discord.Interaction, group: str):
    # URL của nhóm cần lấy thông tin
    url = f"https://hentaihvn.tv/g/{group}"

    # Gửi yêu cầu HTTP đến trang web và lấy HTML
    response = requests.get(url)
    
    # Kiểm tra nếu yêu cầu thành công
    if response.status_code != 200:
        await interaction.response.send_message(f"Không thể lấy thông tin từ {url}.", ephemeral=True)
        return
    
    # Sử dụng BeautifulSoup để phân tích HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        # Lấy src của ảnh nhóm từ HTML
        img_src = soup.find('div', class_='block-item').find('img')['src']
        title = soup.find('h2').text
        description = soup.find('p').text.strip()
        leader = soup.find('span', class_='leader-nhom').a.text
        deputy = soup.find_all('span', class_='leader-nhom')[1].a.text
        # facebook = soup.find_all('a')[2]['href']
        # discord_link = soup.find_all('a')[3]['href']
        likes = soup.find_all('span', class_='face-nhom')[2].text
        budget = soup.find_all('span', class_='face-nhom')[3].text
        top_week = soup.find_all('span', class_='face-nhom')[4].text

        # Tạo embed để hiển thị thông tin nhóm
        embed = discord.Embed(title=title, description=description, color=discord.Color.blue())
        embed.set_thumbnail(url=img_src)  # Hiển thị ảnh nhóm
        embed.add_field(name="Trưởng nhóm", value=leader, inline=True)
        embed.add_field(name="Phó nhóm", value=deputy, inline=True)
        # embed.add_field(name="Facebook", value=f"[Link]({facebook})", inline=False)
        # embed.add_field(name="Discord", value=f"[Link]({discord_link})", inline=False)
        embed.add_field(name="Lượt thích", value=likes, inline=True)
        embed.add_field(name="Ngân sách", value=budget, inline=True)
        embed.add_field(name="Top Tuần", value=top_week, inline=True)

        # Delay 2 giây trước khi gửi
        await asyncio.sleep(2)

        # Gửi thông tin nhóm dưới dạng embed
        await interaction.response.send_message(embed=embed)

    except Exception as e:
        await interaction.response.send_message(f"Đã xảy ra lỗi khi xử lý thông tin: {str(e)}", ephemeral=True)