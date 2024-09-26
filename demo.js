
// README: hãy cài 2 thư viện bên dưới
// Command cmd: npm install discord.js axios cheerio

const axios = require('axios');
const cheerio = require('cheerio');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('check')
        .setDescription('Kiểm tra thông tin nhóm.')
        .addStringOption(option => option.setName('group').setDescription('Tên nhóm')),

    async execute(interaction) {
        const group = interaction.options.getString('group');
        const url = `https://hentaihvn.tv/g/${group}`;

        try {
            const response = await axios.get(url);

            if (response.status !== 200) {
                await interaction.reply({ content: `Không thể lấy thông tin từ ${url}.`, ephemeral: true });
                return;
            }

            const $ = cheerio.load(response.data);

            const imgSrc = $('.block-item img').attr('src');
            const title = $('h2').text();
            const description = $('p').text().trim();
            const leader = $('.leader-nhom').eq(0).find('a').text();
            const deputy = $('.leader-nhom').eq(1).find('a').text();
            const likes = $('.face-nhom').eq(2).text();
            const budget = $('.face-nhom').eq(3).text();
            const topWeek = $('.face-nhom').eq(4).text();

            const embed = new MessageEmbed()
                .setTitle(title)
                .setDescription(description)
                .setColor('BLUE')
                .setThumbnail(imgSrc)
                .addField('Trưởng nhóm', leader, true)
                .addField('Phó nhóm', deputy, true)
                .addField('Lượt thích', likes, true)
                .addField('Ngân sách', budget, true)
                .addField('Top Tuần', topWeek, true);

            // Delay 2 giây trước khi gửi
            setTimeout(async () => {
                await interaction.reply({ embeds: [embed] });
            }, 2000);

        } catch (error) {
            await interaction.reply({ content: `Đã xảy ra lỗi khi xử lý thông tin: ${error.message}`, ephemeral: true });
        }
    }
};